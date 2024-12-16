from fastapi import APIRouter, status, HTTPException, BackgroundTasks, Depends
from ..auth.oauth import require_role
from ..schema.users import GetUsers, Enroll, EnrollResponse
from ..helper.utility import (
    hash_password,
    generate_temp_password,
    find_unapproved_user,
    find_approved_user,
    find_user_in_db,
)
from typing import List
from ..services.send_email import send_approval_message, admin_enrol_user_confirm
from ..models.user import Users


router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get(
    "/get_users",
    status_code=status.HTTP_200_OK,
    response_model=List[GetUsers],
    dependencies=[Depends(require_role("Admin"))],
)
async def get_users():
    users = Users.objects()
    user_dict: List[GetUsers] = [user.to_mongo().to_dict() for user in users]
    return user_dict


@router.post(
    "/approve-user/{email}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_role("Admin"))],
)
async def activate_user(email: str, background_tasks: BackgroundTasks):
    user = find_unapproved_user(email)
    if not user:
        raise HTTPException(status_code=404, detail=f"This user does not exist")

    temp_pwd = generate_temp_password()
    hashed_pwd = hash_password(temp_pwd)

    user.password = hashed_pwd
    user.approved = True
    user.save()
    # send confirmation message to user with temporary password
    background_tasks.add_task(send_approval_message, email, temp_pwd)

    return {"message": "user activated successfully"}


##route to decline user
@router.post("/disapprove-user/{email}", dependencies=[Depends(require_role("Admin"))])
async def deactivate_user(email: str):
    user = find_approved_user(email)
    if user:
        user.approved = False
        user.save()
        # send a message to the user"Your account has been  deactivated
        return {"message": "user deactivated successfully"}


@router.post(
    "/create-user",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "User successfully created.",
            "content": {
                "application/json": {
                    "example": {
                        "message": "User created successfully",
                        "user_id": "abc123",
                    }
                }
            },
        },
        409: {
            "description": "Conflict error if the user already exists.",
            "content": {
                "application/json": {
                    "example": {"detail": "User with this email already exists"}
                }
            },
        },
        422: {"description": "Validation error for invalid input data."},
    },
    summary="Admin can Create A new user based on request.",
    response_model=EnrollResponse,
    description="This endpoint allows admin to create a new user upon which login credentials will be sent to the user mail",
    dependencies=[Depends(require_role("Admin"))],
)
async def create_user(user: Enroll, background_tasks: BackgroundTasks):

    email = user.email
    user_exist = find_user_in_db(email)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with this email already exists",
        )
    temp_pwd = generate_temp_password()
    hashed_pwd = hash_password(temp_pwd)
    new_user = Users(
        fullname=user.fullname,
        email=user.email,
        password=hashed_pwd,
        user_type=user.user_type,
        approved=True,
    )
    new_user.save()

    background_tasks.add_task(admin_enrol_user_confirm, email, temp_pwd)

    return EnrollResponse(id=str(new_user.id), message="User created successfully")

@router.delete("/delete/{email}", dependencies=[Depends(require_role("Admin"))])
async def delete_user(email: str):
    user = find_user_in_db(email)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with email {email} not found")
    user.delete()
    return {"message": f"User with email {email} deleted successfully"}