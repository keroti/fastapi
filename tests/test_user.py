import pytest
from jose import jwt
from app import schemas
from app.config import settings

def test_root(client):
    res = client.get("/")
    print(res.status_code)
    assert res.status_code == 200
    
def test_create_user(client):
    res = client.post("/users/", json={"email":"peterkeroti@gmail.com", "password":"peterkeroti"})
    new_user = schemas.UserOut(**res.json())
    print(res.json())
    assert new_user.email == "peterkeroti@gmail.com"
    assert res.status_code == 201

def test_login(client, test_user):
    res = client.post("/login", data={"username":"peterkeroti@gmail.com","password":test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id= payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize(
    "username, password, status_code",
    [
        ("peter@gmail.com", "peterkeroti", 404),
        ("kigan@gmail.com", "kigan", 404),
        (None, "peterkeroti", 422),
        ("wrongemai@gmail.com", None, 422)
    ]
)
def test_incorrect_login(client, test_user, username, password, status_code):
    res = client.post("/login", data={"username":username,"password":password})
    print(res.json())
    assert res.status_code == status_code
    # assert res.json()["detail"] == "Invalid credentials"