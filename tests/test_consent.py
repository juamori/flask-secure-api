import os, json, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.main import app as flask_app

import pytest

@pytest.fixture
def client(tmp_path, monkeypatch):
    log_path = tmp_path / "consent_test.log"
    monkeypatch.setenv("CONSENT_LOG_PATH", str(log_path))
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as c:
        yield c

def test_consent_endpoint_creates_log(client):
    payload = {"user_id": 123, "version": "v1.0"}
    response = client.post("/consent", json=payload)
    assert response.status_code == 201
    assert response.json == {"status": "ok"}

    log_path = os.environ.get("CONSENT_LOG_PATH")
    assert os.path.exists(log_path)
    with open(log_path, "r", encoding="utf-8") as f:
        data = json.loads(f.read().strip())
    assert data["user_id"] == 123
    assert data["policy_version"] == "v1.0"
    assert "timestamp" in data
