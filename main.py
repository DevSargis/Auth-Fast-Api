from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from configs.logging import setup_logging
from auth.api.health import router as health_router
from auth.api.auth import router as auth_router
from users.api.users import router as user_router
from user_settings.api.user_settings import router as user_settings_router
from users.api.admin import router as admin_router

setup_logging()
load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")
app.include_router(user_settings_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1") 