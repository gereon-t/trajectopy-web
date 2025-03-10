import os

from app.repository import SessionLocal
from app.storage import LocalStorage
from dotenv import load_dotenv

load_dotenv()


def get_storage():
    return LocalStorage(os.getenv("DATA_PATH", "./data"))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
