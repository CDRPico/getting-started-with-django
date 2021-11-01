from django.db import models
from leads.models import *


class Agent(models.Model):
    user = models.OneToOneField('leads.User', on_delete=models.CASCADE)
    organisation = models.ForeignKey('leads.UserProfile', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email