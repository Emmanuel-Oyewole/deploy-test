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
    Query,
)
from fastapi.security import OAuth2PasswordRequestForm

from src.models.user import Users

from ..schema import users, oauth
from ..helper.utility import (
    find_approved_user,
    find_unapproved_user,
    find_user_in_db,
    verify_password,
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
def enroll_user(payload: users.Enroll):
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


@router.post("/login", status_code=status.HTTP_200_OK, response_model=oauth.Token)
def login_user(
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


        #Set the JWT token as a cookie
        response.set_cookie(
            key="access_token",
            value=f"Bearer { access_token }",
            httponly=True,
            samesite="Lax",
            secure=False,
        )

        # response.set_cookie(
        #     key="refresh_token",
        #     value=refresh_token,
        #     httponly=True,
        #     samesite="Lax",
        #     secure=False,
        # )

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




@router.post(
    "/logout",
    summary="Log out user",
    description="This endpoint allows the user to log out by invalidating the JWT tokens.",
    response_description="A message indicating the user has been successfully logged out",
    responses={
        200: {
            "description": "Successfully logged out",
            "content": {
                "application/json": {"example": {"message": "Successfully logged out"}}
            },
        }
    },
)
def logout_user(response: Response):
    """
    Invalidate the JWT token by setting the cookie's expiration to the past
    """
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")

    return {"message": "Successfully logged out"}


from src.auth.oauth import verify_refresh_token


@router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
    summary="Refresh Access Token",
    description="This endpoint allows the user to refresh their access token using a valid refresh token stored in cookies.",
    response_description="A new access token",
    responses={
        200: {
            "description": "Successfully generated a new access token",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "newly_generated_access_token"
                    }
                }
            }
        },
        403: {
            "description": "No refresh token provided",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "No refresh token provided"
                    }
                }
            }
        }
    }
)
def refresh_token(request: Request, response: Response):
    """
    Refresh the access token using a valid refresh token.
    """
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="No refresh token provided"
        )

    payload = verify_refresh_token(refresh_token)

    # Get user_id and role from payload
    user_id = payload.get("sub")
    user_role = payload.get("role")

    # Create new access token
    access_token = create_access_token(
        {"sub": user_id, "role": user_role},
        settings.ACCESS_TOKEN_EXPIRES_MINUTES,
    )

    response.set_cookie(
        key="access_token",
        value=f"Bearer { access_token }",
        httponly=True,
        samesite="Lax",
        secure=False,
    )

    return {"access_token": access_token}


@router.post("/forgot-password/", status_code=status.HTTP_200_OK)
def recover_password(
    background_task: BackgroundTasks, payload: users.forgotPassword = Query(...)
):
    email = payload.email
    user = find_approved_user(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    token = generate_reset_token(email)
    background_task.add_task(send_password_reset_link, email, token)

    return {"message": "Password reset link has been sent to your email"}


@router.post("/reset-password", status_code=status.HTTP_200_OK)
def reset_password(payload: users.ResetPassword):
    token = payload.token
    new_password = payload.new_password
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

    hashed_password = hash_password(new_password)
    user.password = hashed_password
    user.save()

    return {"message": "Password has been reset successfully"}
