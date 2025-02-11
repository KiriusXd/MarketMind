# server/app.py

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from server.database import init_db, SessionLocal, Resource
from server.utils import log_exception
import logging

# Создаем FastAPI приложение
app = FastAPI()

# Инициализация базы данных
init_db()

# Открытие сессии с БД


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Пример API эндпоинта


@app.get("/api/resources")
def get_resources(db: Session = Depends(get_db)):
    try:
        resources = db.query(Resource).all()
        return resources
    except Exception as e:
        log_exception(e)
        return {"message": "Произошла ошибка при получении ресурсов."}


@app.get("/api/resources/{resource_id}")
def get_resource(resource_id: int, db: Session = Depends(get_db)):
    try:
        resource = db.query(Resource).filter(Resource.id == resource_id).first()
        if resource:
            return resource
        return {"message": "Ресурс не найден."}
    except Exception as e:
        log_exception(e)
        return {"message": "Произошла ошибка при получении ресурса."}
