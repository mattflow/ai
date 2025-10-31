from httpx import ASGITransport, AsyncClient
from pydantic import SecretStr
import pytest
from app.main import app
from app.settings import Settings, get_settings
from fastapi import status


@pytest.fixture
def settings():
    return Settings(
        service_user_postgres="test_user",
        service_password_postgres=SecretStr("test_password"),
        service_database_postgres="test_db",
        service_host_postgres="localhost",
        service_port_postgres=5432,
        incremental_database_updates=False,
    )


@pytest.fixture
async def client(settings: Settings):
    def get_settings_override():
        return settings

    app.dependency_overrides[get_settings] = get_settings_override

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest.mark.anyio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}


@pytest.mark.anyio
async def test_redirect_to_docs(client: AsyncClient):
    response = await client.get("/", follow_redirects=False)
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert response.headers["location"] == "/docs"
