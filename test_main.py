import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.database import Base
from app.models import User

# Use the test PostgreSQL database URL
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:grepost5566@127.0.0.1:5432/testdb"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session local class
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup():
    # Create the test database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop the test database tables
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function", autouse=True)
def clear_data():
    # Clear the user table before each test
    db = TestingSessionLocal()
    db.query(User).delete()
    db.commit()
    db.close()

def test_create_user():
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword",
        "profile_info": "Test profile info"
    }

    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    assert response.json() == {
        'status': 'ok',
        'message': 'user created'
    }

    # Verify the user was added to the database
    db = TestingSessionLocal()
    db_user = db.query(User).filter(User.username == "testuser").first()
    assert db_user is not None
    assert db_user.email == "testuser@example.com"
    db.close()

def test_read_user():
    # First, create a user
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword",
        "profile_info": "Test profile info"
    }
    client.post("/users/", json=user_data)

    # Now, read the user
    response = client.get("/users/1")
    assert response.status_code == 200
    user = response.json()
    assert user['username'] == "testuser"
    assert user['email'] == "testuser@example.com"

def test_read_users():
    # First, create multiple users
    users_data = [
        {
            "username": f"testuser{i}",
            "email": f"testuser{i}@example.com",
            "password": "testpassword",
            "profile_info": "Test profile info"
        } for i in range(3)
    ]
    for user_data in users_data:
        client.post("/users/", json=user_data)

    # Now, read the users
    response = client.get("/users/")
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 3

def test_update_user():
    # First, create a user
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword",
        "profile_info": "Test profile info"
    }
    client.post("/users/", json=user_data)

    # Now, update the user
    updated_user_data = {
        "username": "updateduser",
        "email": "updateduser@example.com",
        "password": "newpassword",
        "profile_info": "Updated profile info"
    }
    response = client.put("/users/1", json=updated_user_data)
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user['username'] == "updateduser"
    assert updated_user['email'] == "updateduser@example.com"

def test_delete_user():
    # First, create a user
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword",
        "profile_info": "Test profile info"
    }
    client.post("/users/", json=user_data)

    # Now, delete the user
    response = client.delete("/users/1")
    assert response.status_code == 204

    # Verify the user was deleted
    db = TestingSessionLocal()
    db_user = db.query(User).filter(User.user_id == 1).first()
    assert db_user is None
    db.close()