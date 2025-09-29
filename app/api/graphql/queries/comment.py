import uuid
import strawberry
from typing import List, Optional
from strawberry.types import Info

from app.api.graphql.types.comment import CommentType
from app.services.comment_service import CommentService
from app.utils.graphql_helpers import handle_service_call


@strawberry.type
class CommentQueries:
    @strawberry.field
    def get_comments_for_post(self, info: Info, post_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[CommentType]:
        db = info.context["db"]
        service = CommentService(db)
        return handle_service_call(service.list_comments, post_id, skip, limit)

    @strawberry.field
    def count_comments_for_post(self, info: Info, post_id: uuid.UUID) -> int:
        db = info.context["db"]
        service = CommentService(db)
        return handle_service_call(service.count_comments, post_id)
    
    @strawberry.field
    def get_comment(self, info: Info, comment_id: uuid.UUID) -> Optional[CommentType]:
        db = info.context["db"]
        service = CommentService(db)
        return handle_service_call(service.get_comment, comment_id)
