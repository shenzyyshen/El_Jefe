#settings (db url, api keys secrets)

"""
config.py
Loads environment variables from .env file
"""

from pydantic import BaseSettings

class Settings(BaseSettings):
    """App configuration loaded from .env"""
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    GOOGLE_API_KEY: str | None = None
    OPENAI_API_KEY: str | None = None

    class Config:
        env_file = ".env"
    #PYDANTIC TO LOAD .ENV

# Create global settings instance
settings = Settings()


# Load environment variables from .env
from dotenv import load_dotenv
import os

load_dotenv()

""" Access OpenAI API key"""

OPENAI_API_KEY = os.getenv("OPEN_API_KEY")
DEBUG_MODE = os.getenv("DEBUG", "False").lower() == "true"