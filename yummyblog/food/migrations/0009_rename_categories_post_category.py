# Generated by Django 4.2.2 on 2023-06-17 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0008_alter_category_slug_alter_tags_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='categories',
            new_name='category',
        ),
    ]
