from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import FileStorage, Base

DATABASE_URL = "sqlite:///./data_db.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def initialize_database():
    Base.metadata.create_all(bind=engine)


def get_db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
