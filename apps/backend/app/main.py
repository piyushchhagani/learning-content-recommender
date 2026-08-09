from fastapi import FastAPI

from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=f"{settings.app_name} API",
    description=(
        "AI-powered API for discovering, analyzing, ranking, "
        "and recommending YouTube learning content."
    ),
    version="0.1.0",
)


@app.get("/")
async def root():
    return {
        "name": settings.app_name,
        "version": "0.1.0",
        "environment": settings.app_env,
        "status": "running",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
    }