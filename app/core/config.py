from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")

class Settings(BaseSettings):
    # Application Details
    PROJECT_NAME: str = "Stateless PDF Generator Microservice"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Environment Management (dev, staging, prod)
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Security & Network Settings
    # In production, set this env var to a JSON array or comma-separated list
    # We keep it as a raw string to avoid Pydantic's strict JSON decoding on env vars
    CORS_ORIGINS: str = "*"
    
    # API Key for authentication (required for all PDF generation endpoints)
    # Set via environment variable API_KEY in production
    API_KEY: str = api_key
    API_KEY_HEADER: str = "X-API-Key"
    
    # Tell Pydantic to look for a local .env file first
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        case_sensitive=True
    )

# Instantiate a global settings object to import across your app
settings = Settings()