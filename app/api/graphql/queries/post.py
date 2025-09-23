import uuid
import strawberry
from typing import List, Optional
from strawberry.types import Info

from app.api.graphql.types.post import PostType
from app.services.post_service import PostService

@strawberry.type
class PostQueries:
    @strawberry.field
    def get_post_by_id(self, info: Info, post_id: uuid.UUID) -> Optional[PostType]:
        db = info.context["db"]
        service = PostService(db)
        return service.get_post(post_id)

    @strawberry.field
    def get_posts(self, info: Info, skip: int = 0, limit: int = 100) -> List[PostType]:
        db = info.context["db"]
        service = PostService(db)
        return service.list_posts(skip=skip, limit=limit)
