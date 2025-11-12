import uuid
import strawberry
from typing import Optional
from strawberry.types import Info

from app.models.reaction import ReactionType
from app.api.graphql.types.reaction import ReactionObjectType
from app.services.reaction_service import ReactionService
from app.schemas.reaction import ReactionSet
from app.core.exceptions import AuthenticationError
from app.utils.graphql_helpers import handle_service_call_async

@strawberry.type
class ReactionMutations:
    @strawberry.mutation
    async def set_reaction(self, info: Info, post_id: uuid.UUID, type: ReactionType) -> ReactionObjectType:
        session_manager = info.context["session_manager"]
        user_id = info.context.get("user_id")
        mq_channel = info.context.get("mq_channel")
        if not user_id:
            raise AuthenticationError()
        async with session_manager.get_session() as db:
            service = ReactionService(db, mq_channel)
            reaction_in = ReactionSet(post_id=post_id, type=type)
            return await handle_service_call_async(service.set_reaction, user_id, reaction_in)

    @strawberry.mutation
    async def remove_reaction(self, info: Info, post_id: uuid.UUID) -> Optional[ReactionObjectType]:
        session_manager = info.context["session_manager"]
        user_id = info.context.get("user_id")
        mq_channel = info.context.get("mq_channel")
        if not user_id:
            raise AuthenticationError()
        async with session_manager.get_session() as db:
            service = ReactionService(db, mq_channel)
            return await handle_service_call_async(service.remove_reaction, user_id, post_id)
