from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.logger_config import logger
from app.routes.availability import router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    logger.info("Neon Tide API starting up.")
    yield
    logger.info("Neon Tide API shutting down.")


app = FastAPI(
    title="Neon Tide Night Kayaking API",
    description="Lunar-responsive availability and fleet allocation engine.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)
