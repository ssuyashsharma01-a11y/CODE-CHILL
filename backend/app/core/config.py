from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # 🗄️ Database
    # Using a default that can be overridden by DATABASE_URL in .env
    DATABASE_URL: str = "sqlite:///./trustmark_v6.db"
    
    # 🔐 Authentication & Security
    # In production, these MUST be set in your .env file
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440 
    
    # 👤 Admin Credentials
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str
    
    # 📧 Email Configuration
    EMAIL_USER: str
    EMAIL_PASS: str
    RECEIVER_EMAIL: str
    
    # 👁️ Biometric Thresholds
    FACE_MATCH_THRESHOLD: float = 0.5
    EYE_ASPECT_RATIO_THRESHOLD: float = 0.22
    # Deployment institution name (used for conditional UI fields)
    INSTITUTION_NAME: Optional[str] = "Chandigarh University"

    # Configuration for Pydantic
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    ) 

# Instantiate for use across the app
settings = Settings()