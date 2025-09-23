import strawberry

from app.api.graphql.queries.post import PostQueries
from app.api.graphql.mutations.post import PostMutations

@strawberry.type
class Query(PostQueries):
    pass

@strawberry.type
class Mutation(PostMutations):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)
