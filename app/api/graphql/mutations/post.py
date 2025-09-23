import uuid
import strawberry
from typing import Optional
from strawberry.types import Info

from app.api.graphql.types.post import PostType
from app.services.post_service import PostService
from app.schemas.post import PostCreate, PostUpdate
from app.core.exceptions import AuthenticationError, AppError

@strawberry.type
class PostMutations:
    @strawberry.mutation
    def create_post(self, info: Info, body: str, exercise_ids: Optional[list[uuid.UUID]] = None) -> PostType:
        db = info.context["db"]
        user_id = info.context.get("user_id")
        
        if not user_id:
            raise AuthenticationError()

        service = PostService(db)
        post_in = PostCreate(body=body, exercise_ids=exercise_ids or [])
        return service.create_post(user_id, post_in)

    @strawberry.mutation
    def update_post(self, info: Info, post_id: uuid.UUID, body: Optional[str] = None,
        exercise_ids: Optional[list[uuid.UUID]] = None) -> PostType:
        
        db = info.context["db"]
        user_id = info.context.get("user_id")

        if not user_id:
            raise AuthenticationError()

        service = PostService(db)
        post_in = PostUpdate(body=body, exercise_ids=exercise_ids)

        try:
            return service.update_post(post_id, user_id, post_in)
        except AppError:
            raise

    @strawberry.mutation
    def delete_post(self, info: Info, post_id: uuid.UUID) -> PostType:
        db = info.context["db"]
        user_id = info.context.get("user_id")
        
        if not user_id:
            raise AuthenticationError()

        service = PostService(db)

        try:
            return service.delete_post(post_id, user_id)
        except AppError:
            raise
