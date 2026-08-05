from fastapi import Depends, HTTPException, Header
from fastapi.security import APIKeyHeader
from app.core.config import settings


async def verify_api_key(
    x_api_key: str = Header(..., alias=settings.API_KEY_HEADER)
) -> str:
    """
    Verify the API key from the request header.
    
    Args:
        x_api_key: API key from the X-API-Key header
        
    Returns:
        The valid API key
        
    Raises:
        HTTPException: If the API key is invalid or missing
    """
    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid or missing API key",
        )
    return x_api_key
