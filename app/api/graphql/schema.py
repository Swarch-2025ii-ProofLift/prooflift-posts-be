import strawberry

from app.api.graphql.queries.posts import PostQuery
from app.api.graphql.mutations.posts import PostMutation

@strawberry.type
class Query(PostQuery):
    pass

@strawberry.type
class Mutation(PostMutation):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)
