# tests/test_app.py

import sqlite3
from fastapi.testclient import TestClient
import pytest
from server import app, database
# Переопределяем зависимость get_db для тестирования: используем in-memory SQLite


def override_get_db():
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    # Создаем таблицу ресурсов
    cursor.execute('''
        CREATE TABLE resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            price REAL NOT NULL DEFAULT 0.0
        );
    ''')
    # Вставляем начальные данные
    resources = [
        ("Stone", 1000, 10.0),
        ("Wood", 1000, 5.0),
        ("Iron", 500, 20.0)
    ]
    cursor.executemany("INSERT INTO resources (name, quantity, price) VALUES (?, ?, ?)", resources)
    connection.commit()
    try:
        yield connection
    finally:
        connection.close()


app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Добро пожаловать в MarketMind API на FastAPI!"


def test_get_resources():
    response = client.get("/api/resources")
    assert response.status_code == 200
    resources = response.json()
    # В тестовой базе должно быть 3 ресурса
    assert isinstance(resources, list)
    assert len(resources) == 3
    names = [resource["name"] for resource in resources]
    assert "Stone" in names
    assert "Wood" in names
    assert "Iron" in names


def test_get_resource():
    # Проверяем ресурс с id=1 (Stone)
    response = client.get("/api/resources/1")
    assert response.status_code == 200
    resource = response.json()
    assert resource["id"] == 1
    assert resource["name"] == "Stone"
    assert resource["quantity"] == 1000
    assert resource["price"] == 10.0


def test_update_resource():
    # Обновляем количество ресурса с id=1, например, зададим новое количество = 900
    new_quantity = 900
    response = client.post("/api/resources/1", json={"quantity": new_quantity})
    assert response.status_code == 200
    updated_resource = response.json()
    assert updated_resource["id"] == 1
    assert updated_resource["quantity"] == new_quantity
