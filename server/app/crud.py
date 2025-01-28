from sqlalchemy.orm import Session
from . import models

def add_client_data(db: Session, unique_id: str, checksum: str, public_key: int):
    db_client = models.ClientData(unique_id=unique_id, checksum=checksum, public_key=public_key)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def get_client_data(db: Session, unique_id: str):
    return db.query(models.ClientData).filter(models.ClientData.unique_id == unique_id).first()

def get_all_client_data(db: Session):
    return db.query(models.ClientData).all()

