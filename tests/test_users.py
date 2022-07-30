from fastapi.testclient import TestClient 
from app import schemas
from app.main import app 

#grab our app instance
client = TestClient(app)

def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "hello123@gmail.com", "password": "password123"})

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201