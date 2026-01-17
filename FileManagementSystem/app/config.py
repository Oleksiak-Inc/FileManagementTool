import json
import os
from pathlib import Path
from typing import Dict, Any

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).parent.parent

class Settings(BaseSettings):
    # API Settings
    HOST: str = "0.0.0.0"
    PORT: int = 5000
    
    # Database
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    
    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS: list = ['.txt', '.pdf', '.png', '.jpg', '.jpeg', '.gif', '.csv', '.json', '.xml']
    
    @property
    def UPLOAD_PATH(self) -> Path:
        return BASE_DIR / self.UPLOAD_DIR
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    class Config:
        env_file = ".env"

# Load config from JSON file
def load_json_config() -> Dict[str, Any]:
    config_path = BASE_DIR / "config.json"
    with open(config_path) as f:
        return json.load(f)

# Load JSON config and update env vars
json_config = load_json_config()
os.environ.setdefault("HOST", json_config.get("HOST", "0.0.0.0"))
os.environ.setdefault("PORT", str(json_config.get("PORT", 5000)))
os.environ.setdefault("DB_HOST", json_config.get("DB_HOST", "postgres"))
os.environ.setdefault("DB_PORT", str(json_config.get("DB_PORT", 5432)))
os.environ.setdefault("DB_NAME", json_config.get("DB_NAME", "testarray"))

settings = Settings()

