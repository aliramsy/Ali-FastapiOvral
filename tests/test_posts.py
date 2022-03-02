from urllib import response
from databasetesting import authorized_client,session,client,test_user,token,test_post,test_user1
import schemas
import pytest


def test_get_post(authorized_client,test_post):
    response=authorized_client.get("/post/")
    def verify_post(posts):
        return schemas.Ropost(**posts)
    posts=map(verify_post,response.json())
    posts_list=list(posts)
    print(posts_list)
    assert posts_list[0].Post.title==test_post[0].title
    assert len(test_post)-1==len(response.json())
    assert response.status_code==200
#test_post is sqlalchemy model that is why we can write test_post[0].title


def test_unauthorized_user_get_allposts(client,test_post):
    response=client.get("/post/")
    assert response.status_code==401


def test_unauthorized_user_get_onepost(client,test_post):
    response=client.get(f"/post/{test_post[0].id}")
    assert response.status_code==401


def test_authorized_user_get_onepost(authorized_client,test_post):
    response=authorized_client.get(f"/post/{test_post[0].id}")
    data=response.json()
    data1=schemas.Ropost(**data)
    assert data1.Post.content==test_post[0].content
    assert data["Post"]["title"]==test_post[0].title
    assert response.status_code==200


def test_authorized_user_get_onenonexistpost(authorized_client,test_post):
    response=authorized_client.get("/post/64646")
    assert response.status_code==404


@pytest.mark.parametrize("title,content,status_code",[
    ("4th title","4th content",201),
    ("4th title","5th content",201),
    ("5th title","4th content",201),
    (None,"4th content",422),
    ("4th title",None,422)
])
def test_authorized_user_create_post(authorized_client,test_user,title,content,status_code):
    response=authorized_client.post("/post/",json={"title":title,"content":content,"owner_id":test_user["id"]})
    #posts=schemas.Ropost(**response.json())
    #print(response.json())
    #assert posts.Post.title==title
    #assert posts.Post.content==content
    #assert posts.Post.owner_id==test_user["id"]
    response.status_code==status_code


def test_unauthorized_user_create_post(client):
    response=client.post("/post/",json={"title":"newtitle","content":"new_content"})
    assert response.status_code==401


def test_unauthorized_user_delete_post(client,test_post):
    response=client.delete(f"/post/{test_post[0].id}")
    assert response.status_code==401


def test_authorized_user_delete_post(authorized_client,test_post):
    response=authorized_client.delete(f"/post/{test_post[0].id}")
    assert response.status_code==204


def test_authorized_user_delete_non_exist_post(authorized_client,test_post):
    response=authorized_client.delete(f"/post/64646")
    response.status_code==404


def test_authorized_user_delete_other_users_post(authorized_client,test_post):
    response=authorized_client.delete(f"/post/{test_post[3].id}")
    assert response.status_code==403


def test_unauthorized_user_edit_post(client,test_post):
    data={"title":"new title",
        "content":"new content",
        "id":test_post[0].id
    }
    response=client.put(f"/post/{test_post[0].id}",json=data)
    assert response.status_code==401


def test_authorized_user_edit_post(authorized_client,test_post):
    data={"title":"new title",
        "content":"new content",
        "id":test_post[0].id
    }
    response=authorized_client.put(f"/post/{test_post[0].id}",json=data)
    assert response.status_code==202


def test_authorized_user_edit_non_exist_post(authorized_client,test_post):
    data={"title":"new title",
        "content":"new content",
        "id":test_post[0].id
    }
    response=authorized_client.put(f"/post/64646",json=data)
    response.status_code==404


def test_authorized_user_edit_other_users_post(authorized_client,test_post):
    data={"title":"new title",
        "content":"new content",
        "id":test_post[0].id
    }
    response=authorized_client.put(f"/post/{test_post[3].id}",json=data)
    assert response.status_code==403


