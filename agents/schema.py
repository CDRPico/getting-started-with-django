import random
from graphene_django import DjangoObjectType
import graphene
from graphql import GraphQLError
from graphene_django.forms.mutation import DjangoFormMutation, DjangoModelFormMutation

from .models import Agent as AgentModel
from schema.schema import *
from .forms import AgentModelForm, TestAgentForm

from leads.models import User as UserModel

from graphene import relay

class UserType(DjangoObjectType):
    class Meta:
        model = UserModel

class AgentType(DjangoObjectType):
    class Meta:
        model = AgentModel

class QueryAgents(graphene.ObjectType):
    agents = graphene.List(AgentType)

    def resolve_agents(self, info):
        return AgentModel.objects.all()


class CreateAgent(DjangoFormMutation):
    class Meta:
        form_class = AgentModelForm

    @classmethod
    def perform_mutate(cls, form, info):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password(f"{random.randint(0, 1000000)}")
        user.save()
        AgentModel.objects.create(
            user=user,
            organisation=info.context.user.userprofile
            #organisation=self.request.user.userprofile
        )
        # TODO send email to the created user
        return cls(errors=[], **form.cleaned_data)


class DeleteAgent(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        username=graphene.String()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        agent = AgentModel.objects.get(user__username=kwargs["username"])
        print(agent)
        agent.delete()
        return cls(ok=True)


class UpdateAg(relay.ClientIDMutation):
    class Input:
        username = graphene.String()
        email = graphene.String()
        firstName = graphene.String()
        LastName = graphene.String(required=False, default_value=None)
    
    user = graphene.Field(UserType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        user = UserModel.objects.get(username=kwargs["username"])
        print(user.first_name)
        user.email = kwargs['email']
        user.first_name = kwargs['firstName']
        user.last_name = kwargs['LastName']
        print(user)
        user.save()
        return UpdateAg(user=user)


# class UpdateAgent(DjangoFormMutation):
#     #agent = graphene.Field(AgentType)

#     class Meta:
#         form_class = AgentModelForm

#     @classmethod
#     def perform_mutate(cls, form, info, **kwargs):
#         print("This only runs when the form is valid")
#         print(info.context.user)
#         print(form.cleaned_data)
#         return cls(errors=[], **form.cleaned_data)
        #return UpdateAgent(agent=AgentModel.objects.get(user__username=kwargs["username"]))

    # def resolve_agent(self, info, **kwargs):
    #     agent1 = AgentModel.objects.get(user__username=kwargs["username"])
    #     print(agent1)
    #     return agent1
        # user = form.save(commit=False)
        # print(form.data)
        # agent = AgentModel.objects.get(user__username=form.data['username'])
        # print(agent)
        # user = agent.user
        # user.email = form.data['email']
        # user.first_name = form.data['first_name']
        # user.last_name = form.data['last_name']
        # user.save()
        # agent.user = user
        # agent.save()
        # return cls(errors=[], **form.cleaned_data)
        