# Generated by Django 5.1.2 on 2024-11-20 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0024_alter_event_max_attendee"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="max_attendee",
            field=models.PositiveIntegerField(blank=True, default=None, null=True),
        ),
    ]
