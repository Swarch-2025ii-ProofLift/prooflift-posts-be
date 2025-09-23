from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

db_uri = URL.create(
    drivername=settings.DB_DRIVERNAME,
    username=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_NAME,
)

engine = create_engine(db_uri, echo=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
