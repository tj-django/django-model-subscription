from django.db import models

from model_subscription.mixin import SubscriptionModelMixin


class SubscriptionModel(SubscriptionModelMixin, models.Model):
    class Meta:
        abstract = True
