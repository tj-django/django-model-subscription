from django.db import models
from django.db.models import QuerySet

from model_subscription.mixin import SubscriptionModelMixin


class SubscriptionQuerySet(QuerySet):
    def bulk_create(self, *args, **kwargs):
        objs = super(SubscriptionQuerySet, self).bulk_create(*args, **kwargs)
        self.model.notify_bulk_create(objs)
        return objs

    def update(self, **kwargs):
        rows = super(SubscriptionQuerySet, self).bulk_update(**kwargs)
        self.model.notify_bulk_update(rows)
        return rows

    def delete(self):
        rows = super(SubscriptionQuerySet, self).delete()
        self.model.notify_bulk_delete(rows)
        return rows


class SubscriptionModel(SubscriptionModelMixin, models.Model):
    objects = SubscriptionQuerySet.as_manager()

    class Meta:
        abstract = True
