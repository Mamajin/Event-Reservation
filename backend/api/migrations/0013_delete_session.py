# Generated by Django 5.1.2 on 2024-11-11 06:41

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0012_comment_commentreaction"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Session",
        ),
    ]
