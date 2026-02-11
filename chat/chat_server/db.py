from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = None
SessionLocal = None

class Base(DeclarativeBase):
    pass

def init_db(database_url):
    global engine, SessionLocal
    if database_url:
        engine = create_engine(database_url)
        SessionLocal = sessionmaker(bind=engine)

def get_db():
    return SessionLocal()
