import uuid
import strawberry
from typing import List, Optional
from strawberry.types import Info

from app.api.graphql.types.post import PostType
from app.services.post_service import PostService
from app.utils.graphql_helpers import handle_service_call_async

@strawberry.type
class PostQueries:
    @strawberry.field
    async def get_post_by_id(self, info: Info, post_id: uuid.UUID) -> Optional[PostType]:
        db = info.context["db"]
        service = PostService(db)

        return await handle_service_call_async(service.get_post, post_id)

    @strawberry.field
    async def get_posts(self, info: Info, skip: int = 0, limit: int = 100) -> List[PostType]:
        db = info.context["db"]
        service = PostService(db)

        return await handle_service_call_async(service.list_posts, skip, limit)
    
    @strawberry.field
    async def get_posts_by_user(self, info: Info, user_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[PostType]:
        db = info.context["db"]
        service = PostService(db)

        return await handle_service_call_async(service.list_posts_by_user, user_id, skip, limit)
    
    @strawberry.field
    async def count_posts_by_user(self, info: Info, user_id: uuid.UUID) -> int:
        db = info.context["db"]
        service = PostService(db)

        return await handle_service_call_async(service.count_posts_by_user, user_id)