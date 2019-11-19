from typing import Any, Type

from django.db import models

# Create your models here.
from model_subscription.models import SubscriptionModel


class TestModel(SubscriptionModel):
    name: Type[models.CharField] = models.CharField(max_length=20)

    def __str__(self):
        return '<{}: {}>'.format(self.pk, self.name)
