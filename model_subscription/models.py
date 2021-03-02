from django.conf import settings
from django.db import models, connections
from django.db.models import QuerySet

from model_subscription.mixin import SubscriptionModelMixin


class SubscriptionQuerySet(QuerySet):  # type: ignore
    def bulk_create(self, *args, **kwargs):
        objs = super(SubscriptionQuerySet, self).bulk_create(*args, **kwargs)
        connection = connections[self.db]
        can_notify_bulk_create_subscribers = getattr(
            settings,
            "NOTIFY_BULK_CREATE_SUBSCRIBERS_WITHOUT_PKS",
            connection.features.can_return_ids_from_bulk_insert,
        )
        if can_notify_bulk_create_subscribers:
            self.model.notify_bulk_create(objs)
        return objs

    def update(self, **kwargs):
        rows = super(SubscriptionQuerySet, self).update(**kwargs)
        self.model.notify_bulk_update(self)
        return rows

    def delete(self):
        self.model.notify_bulk_delete(self)
        deleted, rows = super(SubscriptionQuerySet, self).delete()
        return deleted, rows


class SubscriptionModel(  # lgtm [py/conflicting-attributes]
    SubscriptionModelMixin, models.Model
):
    objects = SubscriptionQuerySet.as_manager()

    class Meta:
        abstract = True
