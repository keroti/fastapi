from fastapi.testclient import TestClient
import pytest
from app.main import app
from app import schemas, models
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:99keroti@localhost:5433/test_fastapi'

# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}" # SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

client = TestClient(app)

@pytest.fixture
def session():
    # drop table before code runs
    models.Base.metadata.drop_all(bind=engine)
    # create table before code runs
    models.Base.metadata.create_all(bind=engine)
    # create a new session
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    # Dependency
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db    
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {
        "email":"peterkeroti@gmail.com",
        "password":"peterkeroti"
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {
        "email":"kigan@gmail.com",
        "password":"kigan"
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id":test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user,test_user2, session):
    post_data = [{
        "title":"Test Post 1",
        "content":"Test Content 1",
        "user_id":test_user["id"]
    },
    {
        "title":"Test Post 2",
        "content":"Test Content 2",
        "user_id":test_user["id"]
    },
    {
        "title":"Test Post 3",
        "content":"Test Content 3",
        "user_id":test_user["id"]
    },
    {
        "title":"Test Post 4",
        "content":"Test Content 4",
        "user_id":test_user2["id"]
    }
    ]

    def create_post_model(post):
        return models.Post(**post)
    post_map = map(create_post_model, post_data)
    post = list(post_map)
    session.add_all(post)
    # session.add_all([models.User(title="Test Post 1", content="Test Content 1", user_id=test_user["id"]),
    # models.User(title="Test Post 2", content="Test Content 2", user_id=test_user["id"]),
    # models.User(title="Test Post 3", content="Test Content 3", user_id=test_user["id"]
    # )])
    session.commit()
    posts = session.query(models.Post).all()
    return posts