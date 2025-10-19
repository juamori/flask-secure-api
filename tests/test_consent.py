import sys
import os
import pytest
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app as flask_app

@pytest.fixture
def client():
    """Configura o app para o modo de teste."""
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as c:
        yield c

def test_consent_endpoint_creates_log(client, tmp_path, monkeypatch):
    """
    Verifica se o endpoint /consent grava o log corretamente em um
    diretório temporário, garantindo que o teste não deixe lixo no sistema.
    """
    log_directory = tmp_path
    log_file_path = log_directory / "consent_test.log"

    monkeypatch.setenv('CONSENT_LOG_PATH', str(log_file_path))

    payload = {"user_id": 123, "version": "v1.0"}
    response = client.post("/consent", json=payload)

    assert response.status_code == 201, "A resposta do endpoint /consent deveria ser 201"
    assert response.get_json() == {"status": "ok"}, "O JSON de resposta não está correto"

    assert os.path.exists(log_file_path), f"O arquivo de log esperado não foi encontrado em {log_file_path}"
