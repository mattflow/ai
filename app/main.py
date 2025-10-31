from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.database import create_database_and_tables, get_engine
from app.settings import SettingsDep, get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()

    if settings.incremental_database_updates:
        async with get_engine(settings, echo=True) as engine:
            await create_database_and_tables(engine)

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


@app.get("/health")
async def health_check():
    return {"status": "ok"}
