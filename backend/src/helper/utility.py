from passlib.context import CryptContext
import secrets
import string
from src.models.user import Users
from ..core.config import settings
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


def find_approved_user(email):
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


def create_user_if_not_exists(email, password, fullname, user_type):
    existing_user = Users.objects(email=email).first()
    if not existing_user:
        hashed_password = pwd_context.hash(password)
        user = Users(
            email=email,
            password=hashed_password,
            user_type=user_type,
            approved=True,
            fullname=fullname,
        )
        user.save()
        print(f"{user_type} user created with email: {email}")
    else:
        print(f"{user_type} user already exists with email: {email}")


def create_test_users():
    pwd = settings.GENERAL_PASSWORD
    create_user_if_not_exists(
        email=settings.ADMIN_EMAIL,
        password=pwd,
        fullname=settings.ADMIN_FULLNAME,
        user_type="Admin",
    )

    create_user_if_not_exists(
        email=settings.STUDENT_EMAIL,
        password=pwd,
        fullname=settings.STUDENT_FULLNAME,
        user_type="Student",
    )

    create_user_if_not_exists(
        email=settings.TEACHER_EMAIL,
        password=pwd,
        fullname=settings.TEACHER_FULLNAME,
        user_type="Teacher",
    )

    create_user_if_not_exists(
        email=settings.PARENT_EMAIL,
        password=pwd,
        fullname=settings.PARENT_FULLNAME,
        user_type="Parent",
    )



