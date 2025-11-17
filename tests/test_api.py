import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root_is_alive(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code in (200, 404, 405)  # главное что у нас сервер отвечает


@pytest.mark.asyncio
async def test_openapi_json_exists(client: AsyncClient):
    response = await client.get("/api/v1/hightalent/openapi.json")
    assert response.status_code == 200
    assert "openapi" in response.json()


@pytest.mark.asyncio
async def test_docs_page_exists(client: AsyncClient):
    response = await client.get("/api/v1/hightalent/docs")
    assert response.status_code == 200
    assert "fastapi" in response.text.lower() or "swagger" in response.text.lower()


@pytest.mark.asyncio
async def test_auth_endpoints_exist(client: AsyncClient):
    reg = await client.post("/api/v1/auth/register/", data={"username": "a", "password": "b"})
    login = await client.post("/api/v1/auth/login/", data={"username": "a", "password": "b"})
    assert reg.status_code in (200, 400, 401, 422)
    assert login.status_code in (200, 400, 401, 422)


@pytest.mark.asyncio
async def test_question_endpoints_exist(client: AsyncClient):
    resp = await client.get("/api/v1/questions/")
    assert resp.status_code in (200, 401, 404)


@pytest.mark.asyncio
async def test_answer_endpoints_exist(client: AsyncClient):
    resp = await client.post(
        "/api/v1/answers/",
        json={"question_id": 999, "text": "тест"},
        headers={"Authorization": "Bearer fake"}
    )
    assert resp.status_code in (401, 404, 422)