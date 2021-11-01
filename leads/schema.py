from graphene_django import DjangoObjectType
import graphene
from graphql import GraphQLError

from .models import (
    Lead as LeadModel,
    Category as CategoryModel,
    FollowUp as FollowUpModel
)

class LeadType(DjangoObjectType):
    class Meta:
        model = LeadModel

class FollowUpType(DjangoObjectType):
    class Meta:
        model = FollowUpModel

class CategoryType(DjangoObjectType):
    class Meta:
        model = CategoryModel


class QueryLeads(graphene.ObjectType):
    leads = graphene.List(LeadType)
    leads_assign = graphene.List(
        LeadType,
        assigned = graphene.Boolean()
    )
    leads_detail = graphene.Field(
        LeadType,
        id = graphene.Int()
    )

    def resolve_leads(self, info):
        return LeadModel.objects.all()

    def resolve_leads_assign(self, info, **kwargs):
        assigned=kwargs.get('assigned')
        return LeadModel.objects.filter(agent__isnull=assigned)

    def resolve_leads_detail(self, info, id):
        return LeadModel.objects.get(pk=id)

class QueryCategories(graphene.ObjectType):
    categories = graphene.List(CategoryType)

    def resolve_categories(self, info):
        return CategoryModel.objects.all()

class QueryFollowUps(graphene.ObjectType):
    followups = graphene.List(FollowUpType)

    def resolve_followups(self, info):
        return FollowUpModel.objects.all()