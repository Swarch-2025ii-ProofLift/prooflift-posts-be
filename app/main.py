import uvicorn
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request
from strawberry.fastapi import GraphQLRouter
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.graphql.schema import schema
from app.db.session import get_db, Base, engine
from app.core.exceptions import AuthenticationError
from app.core.security import get_user_id_from_token
from app.mq.message_queue import mq_connection

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting...")

    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created/verified")

    try:
        mq_connection.connect()
        logger.info("MQ connection established")
    except Exception as e:
        logger.warning(f"MQ connection failed: {e}")

    logger.info("Startup complete")

    yield

    logger.info("Shutting down...")

    mq_connection.close()
    logger.info("MQ connection closed")

    engine.dispose()
    logger.info("Database engine disposed")

    logger.info("Application shutdown complete")

async def get_context(request: Request, db=Depends(get_db)):
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
        mq_channel = mq_connection.get_channel()
    except Exception as e:
        logger.warning(f"MQ not available: {e}")

    return {"db": db, "user_id": user_id, "mq_channel": mq_channel}

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

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
