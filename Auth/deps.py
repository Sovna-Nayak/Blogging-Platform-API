from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


DATABASE_URL = ('postgresql://postgres:nayak@localhost:5432/abc')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency

def get_db():
    db = SessionLocal()
    try:
      yield db
    finally:
      db.close()