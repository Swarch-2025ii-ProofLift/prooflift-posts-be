import uvicorn
from fastapi import FastAPI, Depends, Request
from strawberry.fastapi import GraphQLRouter
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.graphql.schema import schema
from app.db.session import get_db, Base, engine
from app.core.exceptions import AuthenticationError
from app.core.security import get_user_id_from_token

Base.metadata.create_all(bind=engine)

async def get_context(request: Request, db=Depends(get_db)):
    user_id = None

    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ", 1)[1]
        try:
            user_id = get_user_id_from_token(token)
        except AuthenticationError:
            pass

    return {"db": db, "user_id": user_id}

graphql_app = GraphQLRouter(
    schema, 
    context_getter=get_context
)

app = FastAPI(
    title=settings.PROJECT_NAME
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
