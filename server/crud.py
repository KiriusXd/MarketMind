from sqlalchemy.orm import Session
from server.models import Resource

# Получение всех ресурсов


def get_resources(db: Session):
    return db.query(Resource).all()

# Получение одного ресурса по id


def get_resource(db: Session, resource_id: int):
    return db.query(Resource).filter(Resource.id == resource_id).first()

# Обновление количества ресурса


def update_resource(db: Session, resource_id: int, quantity: int):
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if resource:
        resource.quantity = quantity
        db.commit()
        db.refresh(resource)
    return resource
