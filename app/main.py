import uvicorn
import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from strawberry.fastapi import GraphQLRouter
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.api.graphql.schema import schema
from app.db.session import Base, engine
from app.db.session_manager import DBSessionManager
from app.core.exceptions import AuthenticationError
from app.core.security import get_user_id_from_token
from app.mq.message_queue import mq_connection

logger = logging.getLogger(__name__)

class TimeoutMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            return await asyncio.wait_for(call_next(request), timeout=55.0)
        except asyncio.TimeoutError:
            logger.error(f"Request timeout: {request.method} {request.url.path}")
            return JSONResponse(
                status_code=504,
                content={"detail": "Request timeout"}
            )

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting...")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created/verified")

    try:
        await mq_connection.connect()
        logger.info("MQ connection established")
    except Exception as e:
        logger.warning(f"MQ connection failed: {e}")

    logger.info("Startup complete")

    yield

    logger.info("Shutting down...")

    await mq_connection.close()
    logger.info("MQ connection closed")

    await engine.dispose()
    logger.info("Database engine disposed")

    logger.info("Application shutdown complete")

async def get_context(request: Request):
    user_id = None
    token = None

    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ", 1)[1]

    if not token:
        token = request.cookies.get("access_token")

    if token:
        try:
            user_id = get_user_id_from_token(token)
        except AuthenticationError:
            pass

    mq_channel = None
    try:
        mq_channel = await mq_connection.get_channel()
    except Exception as e:
        logger.warning(f"MQ not available: {e}")

    session_manager = DBSessionManager()

    return {"session_manager": session_manager, "user_id": user_id, "mq_channel": mq_channel}

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

app.add_middleware(TimeoutMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
async def root():
    return {"message": f"{settings.PROJECT_NAME} is running."}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
