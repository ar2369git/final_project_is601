# tests/integration/test_calculation_crud.py
import pytest
def test_create_power_calc(client):
    # (setup: register & login omitted for brevity)
    token = ...
    headers = {"Authorization": f"Bearer {token}"}
    r = client.post("/calculations", json={"a": 2, "b": 3, "type": "Power"}, headers=headers)
    assert r.status_code == 201
    assert r.json()["result"] == 8

