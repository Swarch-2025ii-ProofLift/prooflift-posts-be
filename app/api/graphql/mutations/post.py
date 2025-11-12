import uuid
import strawberry
from typing import Optional
from strawberry.types import Info

from app.api.graphql.types.post import PostType
from app.services.post_service import PostService
from app.core.exceptions import AuthenticationError
from app.schemas.post import PostCreate, PostUpdate
from app.utils.graphql_helpers import handle_service_call_async

@strawberry.type
class PostMutations:
    @strawberry.mutation
    async def create_post(self, info: Info, body: str, exercise_ids: Optional[list[str]] = None) -> PostType:
        session_manager = info.context["session_manager"]
        user_id = info.context.get("user_id")

        if not user_id:
            raise AuthenticationError()

        async with session_manager.get_session() as db:
            service = PostService(db)
            post_in = PostCreate(body=body, exercise_ids=exercise_ids or [])
            return await handle_service_call_async(service.create_post, user_id, post_in)

    @strawberry.mutation
    async def update_post(self, info: Info, post_id: uuid.UUID, body: Optional[str] = None,
        exercise_ids: Optional[list[str]] = None) -> PostType:
        session_manager = info.context["session_manager"]
        user_id = info.context.get("user_id")

        if not user_id:
            raise AuthenticationError()

        async with session_manager.get_session() as db:
            service = PostService(db)
            post_in = PostUpdate(body=body, exercise_ids=exercise_ids)
            return await handle_service_call_async(service.update_post, post_id, user_id, post_in)

    @strawberry.mutation
    async def delete_post(self, info: Info, post_id: uuid.UUID) -> PostType:
        session_manager = info.context["session_manager"]
        user_id = info.context.get("user_id")

        if not user_id:
            raise AuthenticationError()

        async with session_manager.get_session() as db:
            service = PostService(db)
            return await handle_service_call_async(service.delete_post, post_id, user_id)
