import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app as flask_app
from app.extensions import db


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Cria um cliente Flask isolado com banco de dados em memória."""
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    flask_app.config["TESTING"] = True

    with flask_app.app_context():
        db.create_all()  

    with flask_app.test_client() as c:
        yield c

    with flask_app.app_context():
        db.drop_all()


def test_register_login_protected(client):
    """Testa fluxo completo de registro, login e acesso protegido."""
    rv = client.post('/register', json={'username': 'julia_test', 'password': 'senha123'})
    assert rv.status_code == 201, f"Falha ao registrar: {rv.data}"

    login = client.post('/login', json={'username': 'julia_test', 'password': 'senha123'})
    assert login.status_code == 200, f"Falha no login: {login.data}"
    token = login.get_json().get('access_token')
    assert token, "Token não retornado no login."

    protected = client.get('/protected', headers={'Authorization': f'Bearer {token}'})
    assert protected.status_code == 200
    assert 'Welcome' in protected.get_json().get('message', '')


def test_login_invalid_password(client):
    """Verifica se o login falha com senha incorreta."""
    client.post('/register', json={'username': 'u1', 'password': 'p1'})
    rv = client.post('/login', json={'username': 'u1', 'password': 'wrong'})
    assert rv.status_code == 401
    assert 'invalid credentials' in rv.get_json().get('error', '')


def test_protected_route_no_token(client):
    """Verifica se rota protegida sem token retorna erro 401."""
    rv = client.get('/protected')
    assert rv.status_code == 401
    assert 'missing token' in rv.get_json().get('error', '')
