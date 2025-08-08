# tests/integration/test_calculation_crud.py

import sys
import importlib
import pytest
from pathlib import Path
from fastapi.testclient import TestClient

# Test user credentials
USER_CREDS = {
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "pass1234",
    "confirm_password": "pass1234",
}

@pytest.fixture(autouse=True)
def client(tmp_path, monkeypatch):
    # 1) Point DB_PATH at a fresh file under tmp_path
    db_file = tmp_path / "test.db"
    monkeypatch.setenv("DB_PATH", str(db_file))

    # 2) Remove cached app modules so everything re-imports cleanly
    for mod in (
        "main",
        "app.db",
        "app.models.user",
        "app.models.calculation",
        "app.routers.calculations",
    ):
        if mod in sys.modules:
            del sys.modules[mod]

    # 3) Re-import the DB module and create all tables
    import app.db as db_mod
    import app.models.user    # noqa: F401
    import app.models.calculation  # noqa: F401
    db_mod.init_db()

    # 4) Re-import routers and main so they bind to our fresh DB
    import app.routers.calculations  # noqa: F401
    import main  # noqa: F401

    # 5) As a final safeguard, ensure all metadata is created
    main.Base.metadata.create_all(bind=main.engine)

    # 6) Return a TestClient against the freshly-constructed app
    return TestClient(main.app)

@pytest.fixture
def token(client):
    # Register the test user
    resp = client.post("/register", json=USER_CREDS)
    assert resp.status_code == 200

    # Login to grab a valid JWT
    resp = client.post(
        "/login",
        json={
            "username_or_email": USER_CREDS["username"],
            "password": USER_CREDS["password"],
        },
    )
    assert resp.status_code == 200
    return resp.json()["access_token"]

def test_calculation_crud_flow(client, token):
    headers = {"Authorization": f"Bearer {token}"}

    # CREATE
    r = client.post(
        "/calculations",
        json={"a": 10, "b": 5, "type": "Subtract"},
        headers=headers,
    )
    assert r.status_code == 201
    calc = r.json()
    calc_id = calc["id"]
    assert calc["result"] == 5

    # LIST
    r = client.get("/calculations", headers=headers)
    assert r.status_code == 200
    assert any(c["id"] == calc_id for c in r.json())

    # RETRIEVE
    r = client.get(f"/calculations/{calc_id}", headers=headers)
    assert r.status_code == 200
    assert r.json()["result"] == 5

    # UPDATE
    r = client.put(
        f"/calculations/{calc_id}",
        json={"a": 2, "b": 3, "type": "Multiply"},
        headers=headers,
    )
    assert r.status_code == 200
    assert r.json()["result"] == 6

    # DELETE
    r = client.delete(f"/calculations/{calc_id}", headers=headers)
    assert r.status_code == 204

    # VERIFY DELETION
    r = client.get(f"/calculations/{calc_id}", headers=headers)
    assert r.status_code == 404
