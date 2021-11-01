from graphene.utils.resolve_only_args import resolve_only_args
from graphene_django import  DjangoObjectType
import graphene
from leads.models import Lead as LeadModel

class Lead(DjangoObjectType):
    class Meta:
        model = LeadModel
        fields = (
            "first_name",
            "last_name",
            "age",
            "organisation",
            "agent",
        )

# class LeadType(graphene.ObjectType):
#     leads = graphene.List(Lead)

class Query(graphene.ObjectType):
    leads = graphene.List(Lead)

    def resolve_leads(self, info):
        return LeadModel.objects.all()

schema = graphene.Schema(query=Query)
