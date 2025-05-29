import pytest
from flask import json
from main import app, db, UserModel

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory DB for testing
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Initialize database
        yield client
        with app.app_context():
            db.drop_all()  # Cleanup database

def test_create_user(client):
    response = client.post('/api/users', json={"username": "testuser", "email": "test@example.com"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"

def test_get_all_users(client):
    client.post('/api/users', json={"username": "testuser", "email": "test@example.com"})
    response = client.get('/api/users')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1

def test_get_user_by_id(client):
    client.post('/api/users', json={"username": "testuser", "email": "test@example.com"})
    response = client.get('/api/users/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data["username"] == "testuser"

def test_update_user(client):
    client.post('/api/users', json={"username": "testuser", "email": "test@example.com"})
    response = client.patch('/api/users/1', json={"username": "updateduser", "email": "updated@example.com"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["username"] == "updateduser"

def test_delete_user(client):
    client.post('/api/users', json={"username": "testuser", "email": "test@example.com"})
    response = client.delete('/api/users/1')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 0
