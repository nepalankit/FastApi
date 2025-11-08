from fastapi.testclient import TestClient 
import pytest
from app.main import app
from app.database import get_db, Base
from app.oauth2 import create_access_token
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models
import os
from dotenv import load_dotenv

load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_CONNECTION_URI")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Session ---
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Client ---
@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

# --- User fixture ---
@pytest.fixture
def test_user(client):
    user_data = {"email": "test@example.com", "password": "password123"}
    res = client.post("/users", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

# --- Token fixture ---
@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})

# --- Authorized client ---
@pytest.fixture
def authorized_client(client, token):
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


@pytest.fixture
def test_posts(test_user,session):
    posts_data = [
        {"title": "First Post", "content": "Content of first post", "owner_id": test_user['id']},
        {"title": "Second Post", "content": "Content of second post", "owner_id": test_user['id']},
        {"title": "Third Post", "content": "Content of third post", "owner_id": test_user['id']}
    ]
    
    def create_post_model(post):
        return models.Post(**post)
    post_models = list(map(create_post_model, posts_data))
    
    session.add_all(post_models)
    
    
    # session.add_all([models.Post(title='First Post',content="Content of first post",owner_id=test_user['id']),
    #                  models.Post(title='Second Post',content="Content of second post",owner_id=test_user['id']),
    #                  models.Post(title='Third Post',content="Content of third post",owner_id=test_user['id'])])
    session.commit()
    posts = session.query(models.Post).all()
    return posts