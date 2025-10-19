import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.main import app as flask_app
import pytest

@pytest.fixture
def client(tmp_path, monkeypatch):
    # usa DB temporário em memória para não persistir
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as c:
        yield c

def test_register_login_protected(client):
    # Register
    rv = client.post('/register', json={'username': 'julia', 'password': 'senha123'})
    assert rv.status_code == 201

    # Login
    login = client.post('/login', json={'username': 'julia', 'password': 'senha123'})
    assert login.status_code == 200
    token = login.get_json().get('access_token')
    assert token

    # Protected route with token
    protected = client.get('/protected', headers={'Authorization': f'Bearer {token}'})
    assert protected.status_code == 200
    assert 'Welcome' in protected.get_json().get('message', '')

def test_login_invalid_password(client):
    # create user
    client.post('/register', json={'username': 'u1', 'password': 'p1'})
    rv = client.post('/login', json={'username': 'u1', 'password': 'wrong'})
    assert rv.status_code == 401
    assert 'invalid credentials' in rv.get_json().get('error', '')

def test_protected_route_no_token(client):
    rv = client.get('/protected')
    assert rv.status_code == 401
    assert 'missing token' in rv.get_json().get('error', '')
