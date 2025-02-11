# server/database.py

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from server.utils import log_exception
import os

# URL базы данных (для SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./marketmind.db"

# Инициализация движка SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Создание сессии
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание базы данных и таблиц
Base = declarative_base()

# Определение модели ресурса


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0.0)

# Функция для создания таблиц и инициализации базы данных


def init_db():
    if not os.path.exists('./marketmind.db'):
        print("Создание базы данных и таблиц...")
    else:
        print("Проверка структуры базы данных...")

    try:
        # Создание таблиц, если они еще не существуют
        Base.metadata.create_all(bind=engine)
        print("База данных и таблицы успешно созданы/проверены.")
    except Exception as e:
        log_exception(e)  # Логируем ошибку
        print(f"Ошибка при инициализации базы данных: {e}")
