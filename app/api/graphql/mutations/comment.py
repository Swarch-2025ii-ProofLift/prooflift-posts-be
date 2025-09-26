import uuid
import strawberry
from strawberry.types import Info

from app.api.graphql.types.comment import CommentType
from app.services.comment_service import CommentService
from app.core.exceptions import AuthenticationError
from app.schemas.comment import CommentCreate, CommentUpdate
from app.utils.graphql_helpers import handle_service_call


@strawberry.type
class CommentMutations:
    @strawberry.mutation
    def add_comment(self, info: Info, post_id: uuid.UUID, body: str) -> CommentType:
        db = info.context["db"]
        user_id = info.context.get("user_id")
        if not user_id:
            raise AuthenticationError()
        service = CommentService(db)
        comment_in = CommentCreate(post_id=post_id, body=body)
        return handle_service_call(service.add_comment, user_id, comment_in)

    @strawberry.mutation
    def update_comment(self, info: Info, comment_id: uuid.UUID, body: str) -> CommentType:
        db = info.context["db"]
        user_id = info.context.get("user_id")
        if not user_id:
            raise AuthenticationError()
        service = CommentService(db)
        comment_in = CommentUpdate(body=body)
        return handle_service_call(service.update_comment, comment_id, user_id, comment_in)

    @strawberry.mutation
    def delete_comment(self, info: Info, comment_id: uuid.UUID) -> CommentType:
        db = info.context["db"]
        user_id = info.context.get("user_id")
        if not user_id:
            raise AuthenticationError()
        service = CommentService(db)
        return handle_service_call(service.delete_comment, comment_id, user_id)
