# Generated by Django 4.1.4 on 2023-01-01 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="activity",
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
                ("title", models.CharField(max_length=50)),
                ("content", models.CharField(max_length=255)),
                ("photo", models.CharField(max_length=255)),
                ("create_date", models.DateField(auto_now_add=True)),
            ],
            options={"db_table": "actibity",},
        ),
    ]
