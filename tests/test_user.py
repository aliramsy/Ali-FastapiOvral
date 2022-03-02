from urllib import response
from databasetesting import client,session,test_user
import pytest
from jose import jwt
from config import settings



def test_create_user(client,test_user):
    #response=client.post("/user/",json={"email": "aliusph@gmail.com", "username":"ali", "password":"password123"})
    #data=response.json()
    assert test_user["email"]=="ali@gmail.com"
    assert test_user["username"]=="ali"
    #assert response.status_code==201
    

@pytest.mark.parametrize("email,username, password, status_code",[
 ("ali1@gmail.com", "ali", "password123",409),
 ("ali@gmail.com", "ali1", "password123",409),
 ("ali@gmail.com", "ali", None,422),
 (None, "ali", "password123",422),
 ("ali@gmail.com", None, "password123",422),
 ("ali1@gmail.com", "ali1", "password123",201),
 ("ali@gmail.com", "ali", "password123",409)
])
def test_create_fakeuser(client,test_user,email,username,password,status_code):
    res=client.post("/user/", json={"email": email, "username":username, "password":password})
    assert res.status_code==status_code


def test_get_user(client,session,test_user):
    response=client.get("/user/1")
    data=response.json()
    assert response.status_code==200
    assert data["email"]==test_user["email"]
    assert data["username"]==test_user["username"]

def test_get_all_user(client,session,test_user):
    response=client.get("/user/")
    data=response.json()
    assert response.status_code==200

def test_login(client,session,test_user):
    response=client.post("/login", data={"username":test_user["email"],"password":test_user["password"]})
    data=response.json()
    token=data["access_token"]
    payload:str = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    id=payload.get("user_id")
    assert data["token_type"]=="bearer"
    assert id==test_user["id"]
    assert response.status_code==202

@pytest.mark.parametrize("username, password, status_code",[
 ("ali1@gmail.com", "password123",403),
 ("ali@gmail.com", "password1234",403),
 ("ali1@gmail.com", None,422),
 (None, "password123",422),
 ("ali1@gmail.com", "password1234",403)
])
def test_fakelogin(client,test_user,username,password,status_code):
    response=client.post("/login", data={"username":username,"password":password})
    assert response.status_code==status_code