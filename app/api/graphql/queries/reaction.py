import uuid
import strawberry
from typing import List, Optional
from strawberry.types import Info

from app.models.reaction import ReactionType
from app.api.graphql.types.reaction import ReactionObjectType
from app.services.reaction_service import ReactionService
from app.utils.graphql_helpers import handle_service_call


@strawberry.type
class ReactionQueries:
    @strawberry.field
    def get_reactions_for_post(
        self, info: Info, post_id: uuid.UUID, type: Optional[ReactionType] = None
    ) -> List[ReactionObjectType]:
        db = info.context["db"]
        service = ReactionService(db)
        return handle_service_call(service.list_reactions, post_id, type)

    @strawberry.field
    def count_reactions_for_post(
        self, info: Info, post_id: uuid.UUID, type: Optional[ReactionType] = None
    ) -> int:
        db = info.context["db"]
        service = ReactionService(db)
        return handle_service_call(service.count_reactions, post_id, type)
