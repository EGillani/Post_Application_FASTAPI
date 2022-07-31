from app import schemas
#calling session since client is dependant on it 
from .database import client, session


def test_root(client):
    res = client.get("/")
    assert res.status_code == 200

def test_create_user(client):
    res = client.post(
        "/users", json={"email": "hello123@gmail.com", "password": "password123"})
    
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201
    
