# Generated by Django 5.1.2 on 2024-11-05 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_bookmarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='allowed_email_domains',
            field=models.TextField(blank=True, help_text="Comma-separated list of allowed email domains (e.g., 'ku.th, example.com')", null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='meeting_link',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='visibility',
            field=models.CharField(choices=[('PUBLIC', 'Public'), ('PRIVATE', 'Private')], default='PUBLIC', help_text='Choose whether the event is public or private', max_length=20),
        ),
    ]
