#This is the config for a database solely for testing so we don't touch our development database
#This is also a special file that pytest has - makes the fixtures available throughout the package (no need to import)
import pytest
from fastapi.testclient import TestClient
from app.database import get_db , Base
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.oauth2 import create_access_token
from app import models 
from alembic import command

#make a test database (create it first in postgres)
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost:5432/fastapi_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#the session of the database object 
@pytest.fixture
def session(): 
    #run our code before we run our test - we want to drop the tables and data, and make a brand new one 
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    #if you want to use alembic then use (not using it just to keep things simple)
    #command.upgrade("head")
    db = TestingSessionLocal()
    try:
        yield db
        #here would run our code after our test finishes 
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    #overrides the dependancy (swaps them out) - so we can use the new database 
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    
@pytest.fixture
def test_user(client):
    user_data = {"email": "hello123@gmail.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    #we don't want the hash value cause then it will be encrypted
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def another_test_user(client):
    user_data = {"email": "eve123@gmail.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user



#this is to avoid creating a user, logging in, etc. 
@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


#we need to authenticate our endpoints - no need to manually fill out form
@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


#create a few intial posts so we can test them 
@pytest.fixture
def test_posts(test_user, session, another_test_user):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "user_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "user_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "user_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "user_id": another_test_user['id']
    }]

    def create_post_model(post):
        return models.Post(**post)

    #converting a dictionary and spreading it into a post model
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    #allows multiple entries into a database
    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()
    return posts