from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()

class Settings(BaseSettings):
    # App settings
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool

    #CORS
    CLIENT_ORIGIN: str

    # Database settings
    MONGODB_URL: str 
    DATABASE_NAME: str
    MONGODB_URI: str

    # Email settings
    POSTMARK_SERVER_TOKEN: str
    SENDER_EMAIL: str

    # OAuth settings
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRES_MINUTES: int
    ALGORITHM: str
    REFRESH_TOKEN_EXPIRE_DAYS: int

    #password recovery
    RESET_TOKEN_EXPIRES: int

    #Admin credentials
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str
    ADMIN_FULLNAME: str



    class Config:
        env_file = ".env"

settings = Settings()
