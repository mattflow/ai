from functools import lru_cache
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.responses import RedirectResponse
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    service_user_postgres: str
    service_password_postgres: SecretStr
    service_database_postgres: str
    service_host_postgres: str
    service_port_postgres: int

    @property
    def postgres_sync_url(self) -> SecretStr:
        return SecretStr(
            f"postgresql+psycopg2://{self.service_user_postgres}:"
            f"{self.service_password_postgres.get_secret_value()}@"
            f"{self.service_host_postgres}:"
            f"{self.service_port_postgres}/"
            f"{self.service_database_postgres}"
        )

    @property
    def postgres_async_url(self) -> SecretStr:
        return SecretStr(
            f"postgresql+asyncpg://{self.service_user_postgres}:"
            f"{self.service_password_postgres.get_secret_value()}@"
            f"{self.service_host_postgres}:"
            f"{self.service_port_postgres}/"
            f"{self.service_database_postgres}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()  # pyright: ignore[reportCallIssue]


SettingsDep = Annotated[Settings, Depends(get_settings)]


app = FastAPI()


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/settings")
async def read_settings(settings: SettingsDep):
    return settings
