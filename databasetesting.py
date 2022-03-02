from modulefinder import Module
from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import app
from config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from database import get_db
import pytest
#from alembic import command
from oath import create_access_token
import models


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



#scope="module" means this fixture runs every module
#scope="function" which is defualt one means it runs every test function
#scope="session" means it runs every test session or every time I run pytest
@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    #command.downgrade("base")
    Base.metadata.create_all(bind=engine)
    #command.upgrade("head")
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)



@pytest.fixture
def test_user(client):
    password="password123"
    userdata={"email":"ali@gmail.com","username":"ali","password":password}
    response=client.post("/user/",json=userdata)
    data=response.json()
    data["password"]=password
    print(data)
    return data


@pytest.fixture
def test_user1(client):
    password="password123"
    userdata={"email":"ali123@gmail.com","username":"ali123","password":password}
    response=client.post("/user/",json=userdata)
    data=response.json()
    data["password"]=password
    print(data)
    return data


@pytest.fixture
def token(test_user):
    id=test_user["id"]
    return create_access_token({"user_id":id})


@pytest.fixture
def authorized_client(client,token):
    client.headers={
        **client.headers,
        "Authorization":f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_post(test_user,session,test_user1):
    posts_data = [{
        "title":"first title",
        "content":"first content",
        "owner_id":test_user["id"]},
        {
        "title":"second title",
        "content":"second content",
        "owner_id":test_user["id"]},
        {
        "title":"third title",
        "content":"third content",
        "owner_id":test_user["id"]},
        {
        "title":"first title of new user",
        "content":"first content of new user",
        "owner_id":test_user1["id"]}]
    def create_post_model(posts):
        return models.Post(**posts)
    posts=map(create_post_model,posts_data)
    posts_list=list(posts)
    session.add_all(posts_list)
    session.commit()
    posts=session.query(models.Post).all()
    return posts