from django.db.models.base import ModelBase
from django.utils import six
from django_lifecycle import LifecycleModelMixin, hook

from model_subscription.constants import OperationType
from model_subscription.subscriber import ModelSubscription


class SubscriptionMeta(ModelBase):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    def __new__(cls, name, bases, attrs):
        for base in bases:
            if hasattr(bases, '_subscription'):
                del base['_subscription']
        _subscription = ModelSubscription()
        attrs['_subscription'] = _subscription
        return super(SubscriptionMeta, cls).__new__(cls, name, bases, attrs)


@six.add_metaclass(SubscriptionMeta)
class SubscriptionModelMixin(LifecycleModelMixin):
    def __init__(self, *args, **kwargs):
        self._subscription.subscription_model = self
        self._subscription.auto_discover()
        super(SubscriptionModelMixin, self).__init__(*args, **kwargs)

    @hook('after_create')
    def notify_create(self):
        self._subscription.notify(OperationType.CREATE)

    @hook('after_update')
    def notify_update(self):
        self._subscription.notify(OperationType.UPDATE)

    @hook('after_delete')
    def notify_delete(self):
        self._subscription.notify(OperationType.DELETE)
