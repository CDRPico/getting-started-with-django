# Generated by Django 2.2.24 on 2021-11-01 08:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('agents', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('leads', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='organisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leads.UserProfile'),
        ),
        migrations.AddField(
            model_name='agent',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]