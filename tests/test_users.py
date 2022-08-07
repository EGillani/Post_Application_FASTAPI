
import pytest
from app import schemas
from jose import jwt
from app.config import settings

def test_create_user(client):
    res = client.post(
        "/users", json={"username": "hello123", "password": "password123"})
    
    new_user = schemas.UserOut(**res.json())
    assert new_user.username == "hello123"
    assert res.status_code == 201

def test_create_duplicate_user(test_user,client):

    dup_user = client.post(
        "/users", json={"username": "hello123", "password": "password123"})
    assert dup_user.status_code == 400

#its data because our login is a form (may cause issues if you change the form type)
def test_login_user(test_user, client):
    res = client.post(
        "/token", data={"username": test_user['username'], "password": test_user['password']})
    
    login_res = schemas.Token(**res.json())

    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200
    

@pytest.mark.parametrize("username, password, status_code", [
    ('wrongusername', 'password123', 403),
    ('eve123', 'wrongpassword', 403),
    ('wrongusername', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('eve123', None, 422)
])
def test_incorrect_login(test_user, client, username, password, status_code):
    res = client.post(
        "/token", data={"username": username, "password": password})

    assert res.status_code == status_code