from django.db import models

# Create your models here.
from model_subscription.models import SubscriptionModel


class TestModel(SubscriptionModel):
    name = models.CharField(max_length=20)
