#This is the config for a database solely for testing so we don't touch our development database
import pytest
from fastapi.testclient import TestClient
from app.database import get_db , Base
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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