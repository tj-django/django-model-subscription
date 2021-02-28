import six

from django.conf import settings
from django.db.models.base import ModelBase
from django.core.exceptions import ImproperlyConfigured
from django_lifecycle import LifecycleModelMixin, hook

from model_subscription.constants import OperationType


class SubscriptionMeta(ModelBase):
    """
    The Singleton base metaclass.
    """

    def __new__(mcs, name, bases, attrs):
        from model_subscription.subscriber import ModelSubscription

        for base in bases:
            if hasattr(bases, "_subscription"):
                del base["_subscription"]
        _subscription = ModelSubscription()  # type: ignore
        attrs["_subscription"] = _subscription
        return super(SubscriptionMeta, mcs).__new__(mcs, name, bases, attrs)


@six.add_metaclass(SubscriptionMeta)
class SubscriptionModelMixin(LifecycleModelMixin):
    def __init__(self, *args, **kwargs):
        if getattr(settings, "SUBSCRIPTION_AUTO_DISCOVER", False):
            if not hasattr(settings, "SUBSCRIPTION_MODULE"):
                raise ImproperlyConfigured(
                    "Error no settings.SUBSCRIPTION_MODULE provided."
                )
            self._subscription.auto_discover()
        super(SubscriptionModelMixin, self).__init__(*args, **kwargs)

    @hook("after_create")
    def notify_create(self):
        self._subscription.notify(OperationType.CREATE, self)

    @classmethod
    def notify_bulk_create(cls, objs):
        cls._subscription.notify_many(OperationType.BULK_CREATE, objs)

    @hook("after_update")
    def notify_update(self):
        self._subscription.notify(OperationType.UPDATE, self)

    @classmethod
    def notify_bulk_update(cls, objs):
        cls._subscription.notify_many(OperationType.BULK_UPDATE, objs)

    @hook("after_delete")
    def notify_delete(self):
        self._subscription.notify(OperationType.DELETE, self)

    @classmethod
    def notify_bulk_delete(cls, objs):
        cls._subscription.notify_many(OperationType.BULK_DELETE, objs)
