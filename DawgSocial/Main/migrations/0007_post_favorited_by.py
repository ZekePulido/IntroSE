# Generated by Django 4.2.5 on 2023-11-16 03:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Main', '0005_post_disliked_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='favorited_by',
            field=models.ManyToManyField(blank=True, related_name='favorited_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
