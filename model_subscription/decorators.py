from functools import partial
from typing import Callable, Optional

from django.db import models

from model_subscription.constants import OperationType
from model_subscription.mixin import SubscriptionModelMixin

"""
@subscribe(OperationType.CREATE, TestModel)
def my_custom_receiver(instance)
    pass

@subscribe(OperationType.UPDATE, TestModel)
def my_custom_receiver(instance, updated_data)
    pass

@subscribe(OperationType.DELETE, TestModel)
def my_custom_receiver(instance)
    pass 
"""

"""
@create_subscription(TestModel)
def my_custom_receiver(instance)
    pass


@update_subscription(TestModel)
def my_custom_receiver(instance, updated_data)
    pass


@delete_subscription(TestModel)
def my_custom_receiver(test_instance)
    pass

"""


def subscribe(operation, model):
    # type: ((SubscriptionModelMixin, models.Model), OperationType) -> Callable
    def _decorator(func):
        model._subscription.attach(operation, func)
        return func
    return _decorator


create_subscription = partial(subscribe, OperationType.CREATE)
update_subscription = partial(subscribe, OperationType.UPDATE)
delete_subscription = partial(subscribe, OperationType.DELETE)


def unsubscribe(operation, model, func=None):
    # type: ((SubscriptionModelMixin, models.Model), OperationType, Optional[Callable]) -> Callable

    if func is not None:
        model._subscription.detach(operation, func)
        return func

    def _decorator(inner):
        model._subscription.detach(operation, inner)
        return inner
    return _decorator


unsubscribe_create = partial(unsubscribe, OperationType.CREATE)
unsubscribe_update = partial(unsubscribe, OperationType.UPDATE)
unsubscribe_delete = partial(unsubscribe, OperationType.DELETE)
