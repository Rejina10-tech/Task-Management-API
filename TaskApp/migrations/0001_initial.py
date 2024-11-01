# Generated by Django 5.1.2 on 2024-11-01 05:47

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Task",
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
                ("Title", models.CharField(max_length=100)),
                ("Description", models.TextField(blank=True)),
                ("Date", models.DateField()),
                ("Completed", models.BooleanField(default=False)),
            ],
        ),
    ]