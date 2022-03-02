from urllib import response
from databasetesting import authorized_client,session,client,test_user,token,test_post,test_user1
import models
import pytest


@pytest.fixture
def like_post(authorized_client,session,test_post,test_user):
    likedpost=models.Like(post_id=test_post[1].id,user_id=test_user["id"])
    session.add(likedpost)
    session.commit()
    


def test_like_on_post(authorized_client,test_post):
    response=authorized_client.post("/like/",json={"post_id":test_post[0].id,"dir":1})
    assert response.status_code==201


def test_remove_like_on_post(authorized_client,test_post,like_post):
    response=authorized_client.post("/like/",json={"post_id":test_post[1].id,"dir":0})
    assert response.status_code==201


def test_like_other_user_post(authorized_client,test_post):
    response=authorized_client.post("/like/",json={"post_id":test_post[3].id,"dir":1})
    assert response.status_code==201

def test_like_twice_on_post(authorized_client,test_post,like_post):
    response=authorized_client.post("/like/",json={"post_id":test_post[1].id,"dir":1})
    assert response.status_code==409


def test_remove_like_on_notliked_post(authorized_client,test_post):
    response=authorized_client.post("/like/",json={"post_id":test_post[0].id,"dir":0})
    assert response.status_code==404


def test_like_on_nonexist_post(authorized_client,test_post):
    response=authorized_client.post("/like/",json={"post_id":64646,"dir":1})
    assert response.status_code==404


def test_unauthorized_user_like(client,test_post):
    response=client.post("/like/",json={"post_id":test_post[0].id,"dir":1})
    assert response.status_code==401
