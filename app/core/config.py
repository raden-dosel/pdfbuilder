from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application Details
    PROJECT_NAME: str = "Stateless PDF Generator Microservice"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Environment Management (dev, staging, prod)
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Security & Network Settings
    # Supply as comma-separated origins: "https://my-app.vercel.app,http://localhost:3000"
    CORS_ORIGINS: str = "https://billing-clientside.onrender.com"
    
    # API Key for authentication
    API_KEY: str = "default_dev_key"
    API_KEY_HEADER: str = "X-API-Key"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS string into a list of clean origin strings."""
        if not self.CORS_ORIGINS:
            return ["*"]
        
        raw = self.CORS_ORIGINS.strip()
        
        # Handle JSON array strings like '["https://site.com"]'
        if raw.startswith("["):
            import json
            try:
                parsed = json.loads(raw)
                if isinstance(parsed, list):
                    return [str(item).strip() for item in parsed if item]
            except Exception:
                pass
        
        # Handle comma-separated strings or single domains
        return [origin.strip().strip('"').strip("'") for origin in raw.split(",") if origin.strip()]

    # Pydantic native environment variable configuration
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()