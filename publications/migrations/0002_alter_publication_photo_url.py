# Generated by Django 4.2.1 on 2023-05-09 18:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("publications", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="publication",
            name="photo_url",
            field=models.CharField(null=True),
        ),
    ]
