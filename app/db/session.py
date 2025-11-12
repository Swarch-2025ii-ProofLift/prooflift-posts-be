from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.core.config import settings

db_uri = URL.create(
    drivername=settings.DB_DRIVERNAME,
    username=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_NAME,
)

engine = create_async_engine(
    db_uri,
    echo=False,
    pool_size=10,
    max_overflow=15,
    pool_timeout=30,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_use_lifo=True,
    connect_args={
        "command_timeout": 50,
        "server_settings": {
            "application_name": "prooflift_posts",
            "jit": "off"
        }
    }
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

Base = declarative_base()

async def get_db():
    session = AsyncSessionLocal()
    try:
        yield session
        if session.in_transaction():
            await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
