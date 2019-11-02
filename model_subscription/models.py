from django.db import models
from django.db.models import QuerySet

from model_subscription.mixin import SubscriptionModelMixin


class SubscriptionQuerySet(QuerySet):
    def bulk_create(self, *args, **kwargs):
        # FIX ME
        objs = super(SubscriptionQuerySet, self).bulk_create(*args, **kwargs)
        self.model.notify_bulk_create(self.all())
        return self.all()

    def update(self, **kwargs):
        # FIX ME
        rows = super(SubscriptionQuerySet, self).update(**kwargs)
        self.model.notify_bulk_update(self.all())
        return self.all()

    def delete(self):
        # FIX ME
        deleted, rows = super(SubscriptionQuerySet, self).delete()
        self.model.notify_bulk_delete(self.all())
        return self.all()


class SubscriptionModel(SubscriptionModelMixin, models.Model):
    objects = SubscriptionQuerySet.as_manager()

    class Meta:
        abstract = True
