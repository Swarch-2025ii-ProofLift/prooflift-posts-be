import uuid
import strawberry
from typing import Optional
from strawberry.types import Info

from app.api.graphql.types.reaction import ReactionType
from app.models.reaction import ReactionKind as ReactionKindModel
from app.services.reaction_service import ReactionService
from app.schemas.reaction import ReactionSet
from app.core.exceptions import AuthenticationError
from app.utils.graphql_helpers import handle_service_call


@strawberry.type
class ReactionMutations:
    @strawberry.mutation
    def set_reaction(self, info: Info, post_id: uuid.UUID, kind: ReactionKindModel) -> ReactionType:
        db = info.context["db"]
        user_id = info.context.get("user_id")
        if not user_id:
            raise AuthenticationError()
        service = ReactionService(db)
        reaction_in = ReactionSet(post_id=post_id, kind=kind)
        return handle_service_call(service.set_reaction, user_id, reaction_in)

    @strawberry.mutation
    def remove_reaction(self, info: Info, post_id: uuid.UUID) -> Optional[ReactionType]:
        db = info.context["db"]
        user_id = info.context.get("user_id")
        if not user_id:
            raise AuthenticationError()
        service = ReactionService(db)
        return handle_service_call(service.remove_reaction, user_id, post_id)
