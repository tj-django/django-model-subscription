from functools import partial
from typing import Callable, Optional, Any, Type

from django.conf import settings

from model_subscription.constants import OperationType
from model_subscription.mixin import SubscriptionModelMixin
from model_subscription.types import T

__all__ = [
    "subscribe",
    "create_subscription",
    "bulk_create_subscription",
    "update_subscription",
    "delete_subscription",
    "unsubscribe",
    "unsubscribe_create",
    "unsubscribe_bulk_create",
    "unsubscribe_update",
    "unsubscribe_delete",
    "create_external_subscription",
    "bulk_create_external_subscription",
    "update_external_subscription",
    "bulk_update_external_subscription",
    "delete_external_subscription",
    "bulk_delete_external_subscription",
]


"""
Using the subscribe decorator.

@subscribe(CREATE, TestModel)
def my_custom_create_receiver(instance)
    pass

@subscribe(BULK_CREATE, TestModel)
def my_custom_bulk_create_receiver(instance)
    pass

@subscribe(UPDATE, TestModel)
def my_custom_update_receiver(instance, updated_data)
    pass

@subscribe(DELETE, TestModel)
def my_custom_delete_receiver(instance)
    pass


# (Create, Bulk Create, Update, Delete) decorators

@create_subscription(TestModel)
def my_custom_create_receiver(instance)
    pass

@bulk_create_subscription(TestModel)
def my_custom_bulk_create_receiver(instances):
    pass

@update_subscription(TestModel)
def my_custom_update_receiver(instance, changed_data)
    pass

@delete_subscription(TestModel)
def my_custom_delete_receiver(instance)
    pass

"""


def subscribe(operation, model):
    # type: (OperationType, Type[SubscriptionModelMixin]) -> Callable[[T], None]
    def _decorator(func):
        model._subscription.attach(operation, func)
        return func

    return _decorator


create_subscription = partial(subscribe, OperationType.CREATE)
bulk_create_subscription = partial(subscribe, OperationType.BULK_CREATE)
update_subscription = partial(subscribe, OperationType.UPDATE)
bulk_update_subscription = partial(subscribe, OperationType.BULK_UPDATE)
delete_subscription = partial(subscribe, OperationType.DELETE)
bulk_delete_subscription = partial(subscribe, OperationType.BULK_DELETE)


def unsubscribe(operation, model, func=None):
    # type: (OperationType, Type[SubscriptionModelMixin], Optional[Callable[[T], Any]]) -> Callable[[T], Any]
    if func is not None:
        model._subscription.detach(operation, func)
        return func

    def _decorator(inner):
        model._subscription.detach(operation, inner)
        return inner

    return _decorator


unsubscribe_create = partial(unsubscribe, OperationType.CREATE)
unsubscribe_bulk_create = partial(unsubscribe, OperationType.BULK_CREATE)
unsubscribe_update = partial(unsubscribe, OperationType.UPDATE)
unsubscribe_bulk_update = partial(unsubscribe, OperationType.BULK_UPDATE)
unsubscribe_delete = partial(unsubscribe, OperationType.DELETE)
unsubscribe_bulk_delete = partial(unsubscribe, OperationType.BULK_DELETE)


# Using the settings.SUBSCRIPTION_RUN_EXTERNAL or falls back to settings.DEBUG
def external(func):
    can_run = getattr(settings, "SUBSCRIPTION_RUN_EXTERNAL", settings.DEBUG)
    if not can_run:

        def noop():
            pass

        return noop
    return func


create_external_subscription = external(create_subscription)  # type: ignore
bulk_create_external_subscription = external(bulk_create_subscription)  # type: ignore
update_external_subscription = external(update_subscription)  # type: ignore
bulk_update_external_subscription = external(bulk_update_subscription)  # type: ignore
delete_external_subscription = external(delete_subscription)  # type: ignore
bulk_delete_external_subscription = external(bulk_delete_subscription)  # type: ignore
