# tests/integration/test_calculation_crud.py

import pytest
from fastapi.testclient import TestClient
from app.db import init_db, DB_PATH
from main import app

@pytest.fixture(autouse=True)
def client():
    # Reset the SQLite file before each test
    if DB_PATH.exists():
        DB_PATH.unlink()
    init_db()
    return TestClient(app)

@pytest.fixture
def credentials():
    return {
        "username": "user1",
        "email": "user1@example.com",
        "password": "password123",
        "confirm_password": "password123"
    }

def register_and_get_token(client: TestClient, creds: dict) -> str:
    # Register a new user :contentReference[oaicite:0]{index=0}
    r = client.post("/register", json=creds)
    assert r.status_code == 200

    # Login to obtain JWT :contentReference[oaicite:1]{index=1}
    login_payload = {
        "username_or_email": creds["username"],
        "password": creds["password"]
    }
    r = client.post("/login", json=login_payload)
    assert r.status_code == 200
    body = r.json()
    assert "access_token" in body
    return body["access_token"]

def test_calculation_crud_flow(client: TestClient, credentials: dict):
    token = register_and_get_token(client, credentials)
    headers = {"Authorization": f"Bearer {token}"}

    # CREATE
    create_resp = client.post(
        "/calculations",
        json={"a": 10, "b": 5, "type": "Subtract"},
        headers=headers
    )
    assert create_resp.status_code == 201
    calc = create_resp.json()
    calc_id = calc["id"]
    assert calc["result"] == 5

    # READ LIST
    list_resp = client.get("/calculations", headers=headers)
    assert list_resp.status_code == 200
    assert any(c["id"] == calc_id for c in list_resp.json())

    # READ SINGLE
    get_resp = client.get(f"/calculations/{calc_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["result"] == 5

    # UPDATE
    update_resp = client.put(
        f"/calculations/{calc_id}",
        json={"a": 2, "b": 3, "type": "Multiply"},
        headers=headers
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["result"] == 6

    # DELETE
    del_resp = client.delete(f"/calculations/{calc_id}", headers=headers)
    assert del_resp.status_code == 204

    # VERIFY DELETION
    final_resp = client.get(f"/calculations/{calc_id}", headers=headers)
    assert final_resp.status_code == 404
