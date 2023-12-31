# Generated by Django 4.2.2 on 2023-06-21 14:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('food', '0013_remove_post_comments_commentunderpost_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentunderpost',
            name='dislikes',
            field=models.ManyToManyField(related_name='Дизлайки комментария+', to=settings.AUTH_USER_MODEL, verbose_name='Дизлайки'),
        ),
        migrations.AddField(
            model_name='commentunderpost',
            name='likes',
            field=models.ManyToManyField(related_name='Лайки комментария+', to=settings.AUTH_USER_MODEL, verbose_name='Лайки'),
        ),
    ]
