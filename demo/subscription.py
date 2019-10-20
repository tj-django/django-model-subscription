from demo.models import TestModel
from model_subscription.constants import OperationType
from model_subscription.decorators import subscribe, create_subscription, unsubscribe_create


@subscribe(OperationType.CREATE, TestModel)
def handle_create_1(instance):
    print('1. Created {}'.format(instance.name))


@create_subscription(TestModel)
def handle_create_2(instance):
    print('2. Created {}'.format(instance.name))


unsubscribe_create(TestModel, handle_create_2)
