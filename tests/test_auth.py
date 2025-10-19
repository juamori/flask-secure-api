import sys
import os
import pytest
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app as flask_app

@pytest.fixture
def client():
    """Configura o app para o modo de teste e cria um cliente de teste."""
    flask_app.config['TESTING'] = True
    
    with flask_app.test_client() as c:
        yield c

def test_register_user_success(client):
    """
    Testa APENAS o registro de um *novo* usuário com sucesso.
    Espera um status 201 (Created).
    """
    username = 'successful_user'
    password = 'password123'
    
    rv = client.post('/register', json={
        'username': username,
        'password': password
    })

    assert rv.status_code == 201, "Deveria retornar 201 ao criar um novo usuário"
    assert rv.get_json() is not None, "Deveria retornar um JSON com a resposta"

def test_register_existing_user_fails(client):
    """
    Testa se o registro de um usuário duplicado falha corretamente.
    Isso valida que a API está protegida contra duplicatas.
    """
    username_to_duplicate = 'duplicate_user'
    password = 'password123'

    rv_first = client.post('/register', json={
        'username': username_to_duplicate, 
        'password': password
    })
    assert rv_first.status_code == 201, "O primeiro registro do usuário duplicado deveria funcionar"

    rv_fail = client.post('/register', json={
        'username': username_to_duplicate,
        'password': password
    })

    assert rv_fail.status_code == 400, "Deveria retornar 400 ao tentar registrar um usuário que já existe"

def test_login_and_access_protected_route(client):
    """
    Testa o fluxo completo: registrar, fazer login e acessar uma rota protegida.
    Este teste é autossuficiente.
    """
    username = 'user_for_login_test'
    password = 'senha123'
    
    client.post('/register', json={'username': username, 'password': password})

    rv_login = client.post('/login', json={
        'username': username,
        'password': password
    })
    
    assert rv_login.status_code == 200, "O login deveria retornar 200 com credenciais corretas"
    login_data = rv_login.get_json()
    assert 'access_token' in login_data, "A resposta do login deve conter um 'access_token'"
    
    token = login_data['access_token']

    rv_protected = client.get('/protected', headers={
        'Authorization': f'Bearer {token}'
    })
    
    assert rv_protected.status_code == 200, "Deveria conseguir acessar a rota protegida com um token válido"
    assert username in rv_protected.get_json().get('message', '').lower(), "A mensagem protegida deve conter o nome de usuário"

def test_login_invalid_password(client):
    """
    Testa a falha de login com uma senha incorreta.
    """
    username = 'user_with_wrong_pass'
    correct_password = 'correctpassword'
    wrong_password = 'wrongpassword'

    client.post('/register', json={'username': username, 'password': correct_password})

    rv = client.post('/login', json={
        'username': username,
        'password': wrong_password
    })
    
    assert rv.status_code == 401, "Deveria retornar 401 (Unauthorized) para senha inválida"
    assert 'invalid credentials' in rv.get_json().get('error', ''), "A mensagem de erro para credenciais inválidas não corresponde"

def test_protected_route_no_token(client):
    """
    Testa a falha de acesso a uma rota protegida sem um token de autenticação.
    """
    rv = client.get('/protected')
    
    assert rv.status_code == 401, "Deveria retornar 401 (Unauthorized) quando nenhum token é enviado"
    assert 'missing token' in rv.get_json().get('error', ''), "A mensagem de erro para token ausente não corresponde"
