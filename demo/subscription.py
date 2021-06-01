import logging

from demo.models import TestModel
from model_subscription.constants import OperationType
from model_subscription.decorators import (
    bulk_create_subscription,
    bulk_delete_subscription,
    bulk_update_subscription,
    create_subscription,
    delete_subscription,
    subscribe,
    unsubscribe_create,
    update_subscription,
)

log = logging.getLogger(__name__)


@subscribe(OperationType.CREATE, TestModel)
def handle_create_1(instance):
    log.debug("1. Created {}".format(instance.name))


@create_subscription(TestModel)
def handle_create_2(instance):
    log.debug("2. Created {}".format(instance.name))


unsubscribe_create(TestModel, handle_create_2)


@bulk_create_subscription(TestModel)
def handle_bulk_create(instances):
    for instance in instances:
        log.debug("Bulk Created {}".format(instance.name))


@create_subscription(TestModel)
def handle_create_3(instance):
    log.debug("3. Created {}".format(instance.name))


@update_subscription(TestModel)
def handle_update(instance, changed_data):
    log.debug("Updated {}".format(instance.name))


@bulk_update_subscription(TestModel)
def handle_bulk_update(instances):
    for instance in instances:
        log.debug("Bulk Updated {}".format(instance.name))


@delete_subscription(TestModel)
def handle_delete(instance):
    log.debug("Deleted {}".format(instance.name))


@bulk_delete_subscription(TestModel)
def handle_bulk_delete(instances):
    for instance in instances:
        log.debug("Bulk Deleted {}".format(instance.name))
