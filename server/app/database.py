from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config import settings

DATABASE_URL = f"sqlite:///{settings.DATABASE_URL}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def create_database():
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

