from django.db import models
from django.db.models.deletion import SET_NULL
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from djongo import models as md
from djongo.models.fields import ObjectIdField


class User(AbstractUser):
    is_organisor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
         return self.user.username

class Agent(md.Model):
    _id = md.ObjectIdField()
    user_nickname = md.CharField(max_length=150)
    user_email = md.CharField(max_length=200)
    organisation = md.CharField(max_length=150)

    def __str__(self):
        return self.user_email


class Category(md.Model):
    _id = md.ObjectIdField()
    name = md.CharField(max_length=30)  # New, Contacted, Converted, Unconverted
    # organisation = md.EmbeddedField(
    #     model_container=UserProfile,
    #     on_delete=md.CASCADE
    # )
    organisation = md.CharField(max_length=150)
    #organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    # class Meta:
    #     abstract = False

    def __str__(self):
        return self.name


def handle_upload_follow_ups(instance, filename):
    return f"lead_followups/lead_{instance.lead.pk}/{filename}"


class FollowUp(md.Model):
    # lead = models.ForeignKey(Lead, related_name="followups", on_delete=models.CASCADE)
    date_added = md.DateTimeField(auto_now_add=True)
    notes = md.TextField(blank=True, null=True)
    file = md.FileField(null=True, blank=True, upload_to=handle_upload_follow_ups)

    # def __str__(self):
    #     return f"{self.lead.first_name} {self.lead.last_name}"

    # class Meta:
    #     abstract = True


class LeadManager(md.DjongoManager):
    def get_queryset(self):
        return super().get_queryset()


class Lead(md.Model):
    _id = ObjectIdField()
    first_name = md.CharField(max_length=20)
    last_name = md.CharField(max_length=20)
    age = md.IntegerField(default=0)
    # organisation = md.EmbeddedField(
    #     model_container=UserProfile,
    #     on_delete=md.CASCADE
    # )
    organisation = md.CharField(max_length=150)
    # organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    # agent = md.EmbeddedField(
    #     model_container=Agent,
    #     null=True,
    #     blank=True,
    #     on_delete=md.SET_NULL
    # )
    agent = md.ArrayReferenceField(
        to = Agent,
        null = True,
        blank = True,
        on_delete = SET_NULL
    )
    # agent = models.ForeignKey("Agent", null=True, blank=True, on_delete=models.SET_NULL)
    category = md.EmbeddedField(
        model_container=Category,
        #related_name="leads",
        #null=True,
        #blank=True,
        #on_delete=md.SET_NULL
    )
    # category = models.ForeignKey("Category", related_name="leads", null=True, blank=True, on_delete=models.SET_NULL)
    description = md.TextField()
    date_added = md.DateTimeField(auto_now_add=True)
    phone_number = md.CharField(max_length=20)
    email = md.EmailField()
    profile_picture = md.ImageField(null=True, blank=True, upload_to="profile_pictures/")
    converted_date = md.DateTimeField(null=True, blank=True)

    followups = md.ArrayReferenceField(
        to=FollowUp,
        on_delete=md.SET_NULL,
        null = True,
        blank = True,
    )

    objects = LeadManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=User)