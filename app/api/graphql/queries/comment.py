import uuid
import strawberry
from typing import List, Optional
from strawberry.types import Info

from app.api.graphql.types.comment import CommentType
from app.services.comment_service import CommentService
from app.utils.graphql_helpers import handle_service_call_async

@strawberry.type
class CommentQueries:
    @strawberry.field
    async def get_comments_for_post(self, info: Info, post_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[CommentType]:
        db = info.context["db"]
        service = CommentService(db)
        return await handle_service_call_async(service.list_comments, post_id, skip, limit)

    @strawberry.field
    async def count_comments_for_post(self, info: Info, post_id: uuid.UUID) -> int:
        db = info.context["db"]
        service = CommentService(db)
        return await handle_service_call_async(service.count_comments, post_id)
    
    @strawberry.field
    async def get_comment(self, info: Info, comment_id: uuid.UUID) -> Optional[CommentType]:
        db = info.context["db"]
        service = CommentService(db)
        return await handle_service_call_async(service.get_comment, comment_id)
