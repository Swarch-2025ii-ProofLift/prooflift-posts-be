import uuid
import strawberry
from typing import List, Optional
from strawberry.types import Info

from app.models.reaction import ReactionType
from app.api.graphql.types.reaction import ReactionObjectType
from app.services.reaction_service import ReactionService
from app.utils.graphql_helpers import handle_service_call_async

@strawberry.type
class ReactionQueries:
    @strawberry.field
    async def get_reactions_for_post(
        self, info: Info, post_id: uuid.UUID, type: Optional[ReactionType] = None
    ) -> List[ReactionObjectType]:
        db = info.context["db"]
        service = ReactionService(db)
        return await handle_service_call_async(service.list_reactions, post_id, type)

    @strawberry.field
    async def count_reactions_for_post(
        self, info: Info, post_id: uuid.UUID, type: Optional[ReactionType] = None
    ) -> int:
        db = info.context["db"]
        service = ReactionService(db)
        return await handle_service_call_async(service.count_reactions, post_id, type)
