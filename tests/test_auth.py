import pytest
from app.main import app as flask_app
import json

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as c:
        yield c

def test_register_login_protected(client):
    # Register
    rv = client.post('/register', json={'username':'julia','password':'senha123'})
    assert rv.status_code == 201
    # Login
    rv = client.post('/login', json={'username':'julia','password':'senha123'})
    assert rv.status_code == 200
    token = rv.get_json()['access_token']
    # Protected
    rv = client.get('/protected', headers={'Authorization': f'Bearer {token}'})
    assert rv.status_code == 200
    assert 'hello julia' in rv.get_json()['message']

def test_login_invalid_password(client):
    """
    Testa a falha de login com senha incorreta.
    """
    client.post('/register', json={'username': 'testuser', 'password': 'correctpassword'})
    
    rv = client.post('/login', json={'username': 'testuser', 'password': 'wrongpassword'})
    
    assert rv.status_code == 401
    assert 'invalid credentials' in rv.get_json()['error']

def test_protected_route_no_token(client):
    """
    Testa a falha de acesso a uma rota protegida sem um token.
    """
    rv = client.get('/protected')
    
    assert rv.status_code == 401
    assert 'missing token' in rv.get_json()['error']