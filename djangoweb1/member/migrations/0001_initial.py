# Generated by Django 4.1.4 on 2023-01-06 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Member",
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
                ("name", models.CharField(max_length=50)),
                ("sex", models.CharField(max_length=2)),
                ("birthday", models.DateField()),
                ("email", models.EmailField(max_length=100)),
                ("address", models.CharField(max_length=200)),
                ("password", models.CharField(max_length=200)),
                ("create_date", models.DateField(auto_now_add=True)),
            ],
            options={"db_table": "usermember",},
        ),
    ]
