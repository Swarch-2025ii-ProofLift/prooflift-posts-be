import uuid
from typing import List, Optional, Dict
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.reaction import Reaction, ReactionType
from app.schemas.reaction import ReactionSet


class ReactionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, reaction_id: uuid.UUID) -> Optional[Reaction]:
        result = await self.db.execute(select(Reaction).where(Reaction.id == reaction_id))
        return result.scalar_one_or_none()

    async def get_for_user_post(self, user_id: uuid.UUID, post_id: uuid.UUID) -> Optional[Reaction]:
        result = await self.db.execute(
            select(Reaction).where(Reaction.user_id == user_id, Reaction.post_id == post_id)
        )
        return result.scalar_one_or_none()

    async def get_user_reactions(self, user_id: uuid.UUID, post_ids: List[uuid.UUID]) -> Dict[uuid.UUID, Reaction]:
        query = select(Reaction).where(
            Reaction.user_id == user_id,
            Reaction.post_id.in_(post_ids)
        )
        result = await self.db.execute(query)

        user_reactions = {reaction.post_id: reaction for reaction in result.scalars().all()}
        return user_reactions

    async def set_reaction(self, user_id: uuid.UUID, reaction_in: ReactionSet) -> Reaction:
        db_obj = Reaction(
            post_id=reaction_in.post_id,
            user_id=user_id,
            type=reaction_in.type,
        )
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update_reaction(self, reaction: Reaction, type: ReactionType) -> Reaction:
        reaction.type = type
        await self.db.commit()
        await self.db.refresh(reaction)
        return reaction

    async def remove_reaction(self, reaction: Reaction) -> Reaction:
        await self.db.delete(reaction)
        await self.db.commit()
        return reaction

    async def list_for_post(self, post_id: uuid.UUID, type: Optional[ReactionType] = None) -> List[Reaction]:
        stmt = select(Reaction).where(Reaction.post_id == post_id)
        if type is not None:
            stmt = stmt.where(Reaction.type == type)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def count_for_post(self, post_id: uuid.UUID, type: Optional[ReactionType] = None) -> int:
        stmt = select(func.count()).select_from(Reaction).where(Reaction.post_id == post_id)
        if type is not None:
            stmt = stmt.where(Reaction.type == type)
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def count_for_posts(self, post_ids: List[uuid.UUID], type: Optional[ReactionType] = None) -> dict[uuid.UUID, int]:
        if not post_ids:
            return {}

        stmt = (
            select(Reaction.post_id, func.count(Reaction.id))
            .where(Reaction.post_id.in_(post_ids))
        )
        if type:
            stmt = stmt.where(Reaction.type == type)

        stmt = stmt.group_by(Reaction.post_id)
        result = await self.db.execute(stmt)

        counts = {post_id: 0 for post_id in post_ids}
        counts.update({post_id: count for post_id, count in result.all()})
        return counts

    async def count_by_type_for_post(self, post_id: uuid.UUID) -> Dict[ReactionType, int]:
        stmt = (
            select(Reaction.type, func.count(Reaction.id))
            .where(Reaction.post_id == post_id)
            .group_by(Reaction.type)
        )
        result = await self.db.execute(stmt)
        return {reaction_type: count for reaction_type, count in result.all()}

    async def count_by_type_for_posts(self, post_ids: List[uuid.UUID]) -> Dict[uuid.UUID, Dict[ReactionType, int]]:
        if not post_ids:
            return {}

        stmt = (
            select(Reaction.post_id, Reaction.type, func.count(Reaction.id))
            .where(Reaction.post_id.in_(post_ids))
            .group_by(Reaction.post_id, Reaction.type)
        )
        result = await self.db.execute(stmt)

        counts: Dict[uuid.UUID, Dict[ReactionType, int]] = {}
        for post_id, reaction_type, count in result.all():
            counts.setdefault(post_id, {})[reaction_type] = count
        return counts

