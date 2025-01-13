from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from ..core.config import settings
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.models.user import Users


refresh_token_expiry = settings.REFRESH_TOKEN_EXPIRE_DAYS
algorithm = settings.ALGORITHM
secret_key = settings.SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def user_exist(email):
    get_user = Users.objects(email=email).first()
    if get_user:
        return True
    else:
        return None


def create_refresh_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = (
            datetime.now(timezone.utc) + expires_delta
        )  # Use timezone-aware datetime
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=refresh_token_expiry)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except JWTError:
        return None


####
def create_access_token(data: dict, expires: int):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=algorithm)
    return encoded_jwt


from jose import ExpiredSignatureError
from fastapi import Cookie


def get_current_user(access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(status_code=403, detail="Access token missing")

    try:

        token = access_token.replace("Bearer ", "")
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])

        return payload

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")


from fastapi import HTTPException


def require_role(required_role: str):
    def role_checker(payload: dict = Depends(get_current_user)):
        user_role = payload.get("role")
        if user_role != required_role:
            raise HTTPException(
                status_code=403, detail="Access forbidden: insufficient permissions"
            )

    return role_checker


def check_role(required: str):
    async def role_dependency(user: dict = Depends(get_current_user)):
        if user["role"] != required:
            raise HTTPException(
                status_code=403, detail="Forbidden: You don't have the right role"
            )
        return user

    return role_dependency


def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        if datetime.fromtimestamp(payload["exp"], timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Refresh token has expired")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
