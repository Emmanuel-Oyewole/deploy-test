from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.core.config import settings
from src.routers import auth, admin
from src.helper.utility import create_admin_user
from mongoengine import connect


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to MongoDB
    connect(db=settings.DATABASE_NAME, host=settings.MONGODB_URI)

    # Create admin user during startup
    create_admin_user()

    yield  # Application runs here

    # Clean up resources if needed during shutdown
    print("Application is shutting down.")


app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION, lifespan=lifespan)


origins = [settings.CLIENT_ORIGIN]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def ping():
    return {"Ping": "Pong"}

app.include_router(auth.router)
app.include_router(admin.router)
