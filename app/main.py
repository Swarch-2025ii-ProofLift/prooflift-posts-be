from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from app.core.config import settings
from app.api.graphql.schema import schema

app = FastAPI(
    title=settings.app_name
)

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
async def health_check():
    return {"status": "ok"}
