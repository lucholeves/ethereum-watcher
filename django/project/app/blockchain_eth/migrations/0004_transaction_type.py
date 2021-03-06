# Generated by Django 3.2.7 on 2021-09-23 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("blockchain_eth", "0003_block_number")]

    operations = [
        migrations.AddField(
            model_name="transaction",
            name="type",
            field=models.CharField(
                choices=[
                    ("unknown", "unknown"),
                    ("normal", "normal"),
                    ("internal", "internal"),
                ],
                default="unknown",
                max_length=20,
            ),
        )
    ]
