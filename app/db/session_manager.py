from contextlib import asynccontextmanager
from app.db.session import get_db

class DBSessionManager:
    @asynccontextmanager
    async def get_session(self):
        async for session in get_db():
            yield session
