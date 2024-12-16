from passlib.context import CryptContext
import secrets
import string
from src.models.user import Users
from ..core.config import settings
import bcrypt
from itsdangerous import URLSafeTimedSerializer

serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
reset_token_expiry = settings.RESET_TOKEN_EXPIRES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_reset_token(email: str) -> str:
    return serializer.dumps(email)


def verify_reset_token(token: str) -> str:
    from itsdangerous import SignatureExpired, BadSignature

    try:
        email = serializer.loads(token, max_age=reset_token_expiry)
        return email
    except SignatureExpired:
        return "expired"
    except BadSignature:
        return "invalid"


def hash_refresh_token(token: str) -> str:
    # Hash the refresh token
    hashed = bcrypt.hashpw(token.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def find_approved_user(email: str):
    user = Users.objects(email=email, approved=True).first()
    if user:
        return user
    return None


def find_unapproved_user(email: str):
    user = Users.objects(email=email, approved=False).first()
    if user:
        return user
    return None


def find_user_in_db(email: str):
    user = Users.objects(email=email).first()
    if user:
        return user
    return None


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


def generate_temp_password(length=7) -> str:
    characters = string.ascii_letters + string.digits
    return "".join(secrets.choice(characters) for _ in range(length))


def generate_verification_token() -> int:
    return secrets.randbelow(9000) + 1000


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


# Utility function for admin creation
from src.models.user import Users


def create_admin_user():
    admin_email = settings.ADMIN_EMAIL
    admin_password = settings.ADMIN_PASSWORD
    admin_fullname = settings.ADMIN_FULLNAME

    existing_admin = Users.objects(email=admin_email).first()
    if not existing_admin:
        hashed_password = pwd_context.hash(admin_password)
        admin_user = Users(
            email=admin_email,
            password=hashed_password,
            user_type="Admin",
            approved=True,
            fullname=admin_fullname,
        )
        admin_user.save()
        print(f"Admin user created with email: {admin_email}")
    else:
        print("Admin user already exists.")
