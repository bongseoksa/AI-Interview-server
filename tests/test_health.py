import pytest


@pytest.mark.asyncio
async def test_health_check_returns_200(client):
    response = await client.get("/v1/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ("ok", "degraded")
    assert "database" in data
    assert data["version"] == "0.1.0"


@pytest.mark.asyncio
async def test_health_check_response_schema(client):
    response = await client.get("/v1/health/")
    data = response.json()
    assert set(data.keys()) == {"status", "database", "version"}


@pytest.mark.asyncio
async def test_cors_allows_localhost(client):
    response = await client.options(
        "/v1/health/",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"
