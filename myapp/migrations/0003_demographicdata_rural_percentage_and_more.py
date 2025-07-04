# Generated by Django 5.2 on 2025-04-19 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_census_demographicdata_educationlevel'),
    ]

    operations = [
        migrations.AddField(
            model_name='demographicdata',
            name='rural_percentage',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Pourcentage rural'),
        ),
        migrations.AddField(
            model_name='demographicdata',
            name='urban_percentage',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Pourcentage urbain'),
        ),
    ]
