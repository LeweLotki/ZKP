from sqlalchemy import Column, Integer, String
from app.database import Base

class ClientData(Base):
    __tablename__ = "client_data"

    id = Column(Integer, primary_key=True, index=True)
    unique_id = Column(String, unique=True, index=True)
    checksum = Column(String)
    public_key = Column(Integer)

