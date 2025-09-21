_users = {}

def create_user(username, password_hash):
    if username in _users:
        return False
    _users[username] = {'password': password_hash}
    return True

def get_user(username):
    return _users.get(username)
