# Generated by Django 5.1.2 on 2024-11-10 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_attendeeuser_email_verification_token_sent_at_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='ticket',
            name='api_ticket_ticket__f596c7_idx',
        ),
        migrations.RemoveIndex(
            model_name='ticket',
            name='api_ticket_status_874e9d_idx',
        ),
        migrations.RemoveIndex(
            model_name='ticket',
            name='api_ticket_registe_9c3cbd_idx',
        ),
        migrations.AddField(
            model_name='ticket',
            name='email_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ticket',
            name='user_email',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
    ]
