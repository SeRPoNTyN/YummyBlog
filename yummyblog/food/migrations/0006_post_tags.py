# Generated by Django 4.2.2 on 2023-06-17 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0005_tags_alter_post_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='food.tags', verbose_name='Теги'),
        ),
    ]
