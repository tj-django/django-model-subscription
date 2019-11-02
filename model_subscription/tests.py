import logging

from django.apps import apps
from django.test import TestCase, override_settings, TransactionTestCase

log = logging.getLogger('demo.subscription')


@override_settings(
    SUBSCRIPTION_MODULE='subscription',
    SUBSCRIPTION_AUTO_DISCOVER=True,
)
class ModelSubscriptionTestCase(TestCase):

    @staticmethod
    def get_model(model, app_name='demo'):
        return apps.get_model(app_name, model)

    @classmethod
    def setUpTestData(cls):
        cls.TestModel = cls.get_model('TestModel')


    def test_create_trigger_subscription(self):
        name = 'test'
        with self.assertLogs(log, level=logging.DEBUG) as cm:
            self.TestModel.objects.create(name=name)

        self.assertEqual(
            cm.output,
             [
                 f'DEBUG:demo.subscription:1. Created {name}',
                 f'DEBUG:demo.subscription:3. Created {name}',
             ],
        )

    def test_update_triggers_subscription(self):
        name = 'test'
        new_name = 'New name'
        with self.assertLogs(log, level=logging.DEBUG) as cm:
            t = self.TestModel.objects.create(name=name)

            self.assertEqual(t.name, 'test')

            # Update
            t.name = new_name
            t.save()

        self.assertEqual(
            cm.output,
            [
                f'DEBUG:demo.subscription:1. Created {name}',
                f'DEBUG:demo.subscription:3. Created {name}',
                f'DEBUG:demo.subscription:Updated {new_name}',
            ],
        )

@override_settings(
    SUBSCRIPTION_MODULE='subscription',
    SUBSCRIPTION_AUTO_DISCOVER=True,
)
class ModelSubscriptionTransactionTestCase(TransactionTestCase):
    @staticmethod
    def get_model(model, app_name='demo'):
        return apps.get_model(app_name, model)

    def setUp(self) -> None:
        self.TestModel = self.get_model('TestModel')

    def test_bulk_create_triggers_subscription(self):
        names = [
            'new-{v}'.format(v=i) for i in range(100)
        ]
        # Bulk create
        with self.assertLogs(log, level=logging.DEBUG) as cm:
            objs = self.TestModel.objects.bulk_create([
                self.TestModel(name=name) for name in names
            ])

        self.assertEqual(
            cm.output,
            [
                f'DEBUG:demo.subscription:Bulk Created {name}'
                for name in names
            ],
        )

    def test_bulk_update_tirggers_subscription(self):
        names = [
            'new-{v}'.format(v=i) for i in range(100)
        ]
        # Bulk create
        with self.assertLogs(log, level=logging.DEBUG) as cm:
            objs = self.TestModel.objects.bulk_create([
                self.TestModel(name=name) for name in names
            ])

        self.assertEqual(
            cm.output,
            [
                f'DEBUG:demo.subscription:Bulk Created {name}'
                for name in names
            ]
        )
        new_name = 'new'

        with self.assertLogs(log, level=logging.DEBUG) as cm:
            self.TestModel.objects.filter(id__in=[obj.pk for obj in objs]).update(name=new_name)

        self.assertEqual(
            cm.output,
            [
                f'DEBUG:demo.subscription:Bulk Updated {new_name}'
                for name in names
            ]
        )
