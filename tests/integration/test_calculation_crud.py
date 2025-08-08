# tests/integration/test_calculation_crud.py

import pytest
from fastapi.testclient import TestClient
from app.db import init_db, DB_PATH
from main import app

@pytest.fixture(autouse=True)
def client():
    # Reset the SQLite file each time :contentReference[oaicite:0]{index=0}
    if DB_PATH.exists():
        DB_PATH.unlink()
    init_db()
    return TestClient(app)

@pytest.fixture
def user_creds():
    return {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "pass1234",
        "confirm_password": "pass1234"
    }

@pytest.fixture
def token(client, user_creds):
    # Register the user :contentReference[oaicite:1]{index=1}
    reg = client.post("/register", json=user_creds)
    assert reg.status_code == 200

    # Login to get JWT :contentReference[oaicite:2]{index=2}
    login_resp = client.post(
        "/login",
        json={
            "username_or_email": user_creds["username"],
            "password": user_creds["password"]
        }
    )
    assert login_resp.status_code == 200
    return login_resp.json()["access_token"]

def test_calculation_crud_flow(client, token):
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

    # LIST
    list_resp = client.get("/calculations", headers=headers)
    assert list_resp.status_code == 200
    assert any(c["id"] == calc_id for c in list_resp.json())

    # RETRIEVE SINGLE
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
