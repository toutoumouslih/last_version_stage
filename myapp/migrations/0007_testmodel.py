# Generated by Django 5.1.7 on 2025-05-27 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0006_alter_demographicdata_unique_together"),
    ]

    operations = [
        migrations.CreateModel(
            name="TestModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
        ),
    ]
