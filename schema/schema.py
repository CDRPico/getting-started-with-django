from django.db.models import fields, query
from graphene.utils.resolve_only_args import resolve_only_args
from graphene_django import  DjangoObjectType, DjangoConnectionField, DjangoListField
import graphene
from leads.models import (
    Lead as LeadModel,
    Agent as AgentModel,
    User as UserModel,
    UserProfile as UserProfileModel,
    FollowUp as FollowUpModel,
    Category as CategoryModel
)
from agents.schema import (
    UserType,
    QueryAgents,
    CreateAgent,
    DeleteAgent,
    UpdateAg
)
from leads.schema import (
    LeadType,
    CategoryType,
    FollowUpType,
    QueryCategories,
    QueryFollowUps,
    QueryLeads
)


# class UserType(DjangoObjectType):
#     class Meta:
#         model = UserModel


class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfileModel


class Query(QueryAgents, 
            QueryLeads,
            QueryCategories,
            QueryFollowUps,
            graphene.ObjectType):
    user = graphene.Field(
        UserType,
        )
    user_detail = graphene.Field(
        UserType,
        id = graphene.Int()
    )

    def resolve_users(self, info):
        return UserModel.objects.all()

    def resolve_user_detail(self, info, id):
        return UserModel.objects.get(pk=id)


class Mutation(graphene.ObjectType):
    agent_create = CreateAgent.Field()
    agent_delete = DeleteAgent.Field()
    agent_update = UpdateAg.Field()



schema = graphene.Schema(query=Query, mutation=Mutation)


