from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine

from app.models import Model
from app.settings import Settings, SettingsDep


@asynccontextmanager
async def get_engine(settings: Settings, echo: bool = False):
    engine = create_async_engine(
        settings.postgres_async_url.get_secret_value(), echo=echo
    )
    try:
        yield engine
    finally:
        await engine.dispose()


async def get_engine_dep(settings: SettingsDep):
    async with get_engine(settings) as engine:
        yield engine


EngineDep = Annotated[AsyncEngine, Depends(get_engine_dep)]


async def get_session(engine: EngineDep):
    async with AsyncSession(engine) as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def create_database_and_tables(engine: AsyncEngine):
    async with engine.begin() as connection:
        await connection.run_sync(Model.metadata.create_all)
