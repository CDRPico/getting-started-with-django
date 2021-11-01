from graphene_django import DjangoObjectType
import graphene
from graphql import GraphQLError

from .models import Agent as AgentModel

class AgentType(DjangoObjectType):
    class Meta:
        model = AgentModel

class QueryAgents(graphene.ObjectType):
    agents = graphene.List(AgentType)

    def resolve_agents(self, info):
        return AgentModel.objects.all()