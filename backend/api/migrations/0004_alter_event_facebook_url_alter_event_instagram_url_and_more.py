# Generated by Django 5.1.2 on 2024-10-31 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_event_address_alter_event_dress_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='facebook_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='instagram_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='twitter_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='website_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
