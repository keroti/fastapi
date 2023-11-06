import pytest
from typing import List
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unauthorized_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 200

def test_unauthorized_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 200

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id + 100}")
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.Post(**res.json())
    assert post.id == test_posts[0].id
    assert post.title == test_posts[0].title
    assert post.content == test_posts[0].content
    assert res.status_code == 200
    assert res.json()["id"] == test_posts[0].id

@pytest.mark.parametrize("title, content, published", [
    ("Awsome new title", "Awsome new content", True),
    ("Favorite resturant", "I love Manara in Nairobi", False),
    ("My age", "I'm old enough to be an adult", True),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    assert res.status_code == 201

    created_post = schemas.Post(**res.json())
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.user_id == test_user["id"]

def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json={"title": "Awsome new title", "content": "Awsome new content"})
    assert res.status_code == 201

    created_post = schemas.Post(**res.json())
    assert created_post.title == "Awsome new title"
    assert created_post.content == "Awsome new content"
    assert created_post.published == True
    assert created_post.user_id == test_user["id"]

    created_post = schemas.Post(**res.json())
    assert created_post.published == True

def test_create_post_unauthorized(client, test_user, test_posts):
    res = client.post("/posts/", json={"title": "Awsome new title", "content": "Awsome new content"})
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_not_exist(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id + 100}")
    assert res.status_code == 404

def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_other_user_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update_post(authorized_client, test_posts):
    data = {
        "title": "Updated title",
        "content": "Updated content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]

def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "Updated title",
        "content": "Updated content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403

def test_unauthorized_user_update_post(client, test_user, test_user2, test_posts):
    data = {
        "title": "Updated title",
        "content": "Updated content",
        "id": test_posts[0].id
    }
    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 401

def test_update_post_not_exist(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "Updated title",
        "content": "Updated content",
        "id": test_posts[0].id + 100
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id + 100}", json=data)
    assert res.status_code == 404