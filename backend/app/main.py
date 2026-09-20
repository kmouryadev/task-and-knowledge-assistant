from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.health import router as health_router
from app.core.errors import register_error_handlers
from app.core.logging import configure_logging, get_logger
from app.core.settings import get_settings

configure_logging()
logger = get_logger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("app_startup", environment=settings.environment)
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

register_error_handlers(app)
app.include_router(health_router)
