import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import router as pdf_router
from app.core.config import settings

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# CORS origins are sourced from settings so they can differ per
# environment (permissive in dev, locked down in production).
# Coerce CORS origins into a list if settings provides a string
cors_origins = settings.CORS_ORIGINS
if isinstance(cors_origins, str):
    cors_str = cors_origins.strip()
    if cors_str.startswith("["):
        import json
        try:
            cors_list = json.loads(cors_str)
        except Exception:
            cors_list = [item.strip() for item in cors_str.strip("[]").split(",") if item.strip()]
    else:
        cors_list = [item.strip() for item in cors_str.split(",") if item.strip()]
else:
    cors_list = cors_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],    
)

app.include_router(pdf_router)


@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "healthy", "environment": settings.ENVIRONMENT}


