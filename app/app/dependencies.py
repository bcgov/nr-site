
from .database import SessionLocal, engine



def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
