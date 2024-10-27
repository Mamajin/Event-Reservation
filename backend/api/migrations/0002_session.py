# Generated by Django 5.1.2 on 2024-10-23 11:14

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_name', models.CharField(max_length=255)),
                ('event_create_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Session Created At')),
                ('start_date_event', models.DateTimeField(verbose_name='Session Start Date')),
                ('end_date_event', models.DateTimeField(blank=True, verbose_name='Session End Date')),
                ('start_date_register', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Registration Start Date')),
                ('end_date_register', models.DateTimeField(verbose_name='Registration End Date')),
                ('description', models.TextField(max_length=400)),
                ('max_attendee', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('session_type', models.CharField(max_length=100)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='api.event')),
            ],
        ),
    ]
