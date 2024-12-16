from datetime import datetime, timedelta, timezone
import bcrypt

from typing import Annotated

from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Depends,
    Response,
    Request,
    BackgroundTasks,
)
from fastapi.security import OAuth2PasswordRequestForm

from src.models.user import Users

from ..schema import users, oauth
from ..helper.utility import (
    find_approved_user,
    find_unapproved_user,
    find_user_in_db,
    verify_password,
    hash_refresh_token,
    generate_reset_token,
    verify_reset_token,
    hash_password,
)
from ..services.send_email import send_password_reset_link
from ..auth.oauth import create_access_token, create_refresh_token
from ..core.config import settings


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/enroll", status_code=status.HTTP_201_CREATED, response_model=users.EnrollResponse
)
async def enroll_user(payload: users.Enroll):
    approved_user_exist = find_approved_user(payload.email)
    if approved_user_exist:
        raise HTTPException(
            status_code=409,
            detail="This account has already been created and approved by the admin",
        )

    unapproved_user_exist = find_unapproved_user(payload.email)

    if unapproved_user_exist:
        raise HTTPException(
            status_code=409,
            detail=f"This account has already been created and is pending approval",
        )
    new_user = Users(
        fullname=payload.fullname, email=payload.email, user_type=payload.user_type
    )
    new_user.save()

    return {"user_id": str(new_user.user_id), "message": "success"}


@router.post("/login", response_model=oauth.Token)
async def login_user(
    payload: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
    request: Request,
):
    try:
        # Check for an active session
        active_session = request.cookies.get("access_token")
        if active_session:
            raise HTTPException(
                status_code=403, detail="User is currently in an active session"
            )

        email = payload.username
        password = payload.password

        # Find user in the database
        user_in_db = find_user_in_db(email)
        approved_user = find_approved_user(email)

        # Validate user credentials and account status
        if not user_in_db:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
            )
        if user_in_db and not approved_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User account is not approved, await approval from admin",
            )

        # Authenticate user
        if not verify_password(password, approved_user.password):
            raise HTTPException(status_code=404, detail="Invalid credentials")

        # Create access token
        access_token = create_access_token(
            {"sub": str(approved_user.user_id), "role": approved_user.user_type},
            settings.ACCESS_TOKEN_EXPIRES_MINUTES,
        )

        # create_refresh_token = create_refresh_token
        refresh_token = create_refresh_token(
            data={"sub": str(approved_user.user_id), "role": approved_user.user_type}
        )

        hashed_refresh_token = hash_refresh_token(refresh_token)
        approved_user.refresh_token = hashed_refresh_token
        approved_user.refresh_token_expiry = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
        approved_user.save()

        # Set the JWT token as a cookie
        response.set_cookie(
            key="access_token",
            value=f"Bearer { access_token }",
            httponly=True,  # Ensure the cookie is not accessible via JavaScript
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "id": str(approved_user.user_id),
        }

    except HTTPException as http_exc:
        raise http_exc  # Re-raise the HTTPException to return the appropriate response

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )


@router.post("/logout")
async def logout_user(response: Response):
    # Invalidate the JWT token by setting the cookie's expiration to the past
    response.set_cookie(
        key="access_token",
        value="",
        expires=0,  # Set expiration to 0 to delete the cookie
        httponly=True,  # Ensure the cookie is not accessible via JavaScript
    )

    return {"message": "Successfully logged out"}


@router.post("/refresh")
async def refresh_token(user_id: str, refresh_token: str):
    # Find the user by user ID
    user = Users.objects(user_id=user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Verify the provided refresh token against the stored hash
    if not bcrypt.checkpw(
        refresh_token.encode("utf-8"), user.refresh_token.encode("utf-8")
    ):

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid refresh token"
        )

    if user.refresh_token_expiry < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Expired refresh token"
        )

    # Create a new access token
    access_token = create_access_token(
        {"sub": user.user_id, "role": user.user_type},
        settings.ACCESS_TOKEN_EXPIRES_MINUTES,
    )

    # Optionally, create a new refresh token and update the database
    new_refresh_token = create_refresh_token(data={"sub": user.user_id})
    user.refresh_token_hash = hash_refresh_token(new_refresh_token)
    user.refresh_token_expires = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES
    )
    user.save()

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }


@router.post("/forgot-password")
def recover_password(email: str, background_task: BackgroundTasks):
    user = find_approved_user(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    token = generate_reset_token(email)
    background_task.add_task(send_password_reset_link, email, token)

    return {"message": "Password reset link has been sent to your email"}


@router.post("/reset-password")
def reset_password(token: str, new_password: str):
    email = verify_reset_token(token)
    if email == "expired":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Reset token has expired"
        )

    if email == "invalid":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid reset token"
        )

    user = find_approved_user(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    hashed_password = hash_password(new_password)
    user.password = hashed_password
    user.save()

    return {"message": "Password has been reset successfully"}
