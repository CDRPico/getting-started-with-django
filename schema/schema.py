from django.db.models import fields, query
from graphene.utils.resolve_only_args import resolve_only_args
from graphene_django import  DjangoObjectType, DjangoConnectionField, DjangoListField
import graphene
from leads.models import (
    Lead as LeadModel,
    Agent as AgentModel,
    User as UserModel,
    FollowUp as FollowUpModel,
    Category as CategoryModel
)
from agents.schema import (
    AgentType,
    QueryAgents
)
from leads.schema import (
    LeadType,
    CategoryType,
    FollowUpType,
    QueryCategories,
    QueryFollowUps,
    QueryLeads
)

class UserType(DjangoObjectType):
    class Meta:
        model = UserModel


class Query(QueryAgents, 
            QueryLeads,
            QueryCategories,
            QueryFollowUps,
            graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
