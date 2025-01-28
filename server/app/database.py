from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config import settings

# Database URL and connection
DATABASE_URL = f"sqlite:///{settings.DATABASE_URL}"

# Create engine and session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the Base object that will be used by your models
Base = declarative_base()

# Function to create the tables
def create_database():
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

