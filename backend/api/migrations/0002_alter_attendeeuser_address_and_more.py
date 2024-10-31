# Generated by Django 5.1 on 2024-10-31 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendeeuser',
            name='address',
            field=models.CharField(blank=True, default=' ', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='attendeeuser',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, default=0.0, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='attendeeuser',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, default=0.0, max_digits=9, null=True),
        ),
    ]
