# Generated by Django 2.2.6 on 2019-10-20 16:27

from django.db import migrations, models

import model_subscription.mixin


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TestModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20)),
            ],
            options={
                "abstract": False,
            },
            bases=(model_subscription.mixin.SubscriptionModelMixin, models.Model),
        ),
    ]
