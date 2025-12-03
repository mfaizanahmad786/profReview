"""
Configuration Management
This file loads environment variables and provides them to the application.
We use python-dotenv to read from .env file.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    BaseSettings automatically reads from .env file.
    """
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create a single instance to be imported throughout the app
settings = Settings()

