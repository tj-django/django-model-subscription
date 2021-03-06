import logging

from django.apps import apps
from django.db import connections
from django.test import TestCase, override_settings, TransactionTestCase

log = logging.getLogger("demo.subscription")


@override_settings(
    SUBSCRIPTION_MODULE="subscription",
    SUBSCRIPTION_AUTO_DISCOVER=False,
)
class ModelSubscriptionTestCase(TestCase):
    @staticmethod
    def get_model(model, app_name="demo"):
        return apps.get_model(app_name, model)

    @classmethod
    def setUpTestData(cls):
        cls.TestModel = cls.get_model("TestModel")

    def test_create_triggers_subscription(self):
        name = "test"
        with self.assertLogs(log, level=logging.DEBUG) as cm:
            self.TestModel.objects.create(name=name)

        self.assertEqual(
            cm.output,
            [
                "DEBUG:demo.subscription:1. Created {}".format(name),
                "DEBUG:demo.subscription:3. Created {}".format(name),
            ],
        )

    def test_update_triggers_subscription(self):
        name = "test"
        new_name = "New name"
        with self.assertLogs(log, level=logging.DEBUG) as cm:
            t = self.TestModel.objects.create(name=name)

            self.assertEqual(t.name, name)

            # Update
            t.name = new_name
            t.save()

        self.assertEqual(
            cm.output,
            [
                "DEBUG:demo.subscription:1. Created {}".format(name),
                "DEBUG:demo.subscription:3. Created {}".format(name),
                "DEBUG:demo.subscription:Updated {}".format(new_name),
            ],
        )

    def test_delete_triggers_subscription(self):
        name = "test"
        with self.assertLogs(log, level=logging.DEBUG) as cm:
            t = self.TestModel.objects.create(name=name)

            self.assertEqual(t.name, name)

            t.delete()

        self.assertEqual(
            cm.output,
            [
                "DEBUG:demo.subscription:1. Created {}".format(name),
                "DEBUG:demo.subscription:3. Created {}".format(name),
                "DEBUG:demo.subscription:Deleted {}".format(name),
            ],
        )


class BaseSubscriptionTransactionTestCase(TransactionTestCase):
    @staticmethod
    def get_model(model, app_name="demo"):
        return apps.get_model(app_name, model)

    @classmethod
    def setUpClass(cls):
        super(BaseSubscriptionTransactionTestCase, cls).setUpClass()
        cls.TestModel = cls.get_model("TestModel")


@override_settings(
    SUBSCRIPTION_MODULE="subscription",
    SUBSCRIPTION_AUTO_DISCOVER=False,
)
class ModelSubscriptionSqliteTransactionTestCase(BaseSubscriptionTransactionTestCase):
    db_alias = "default"

    @override_settings(NOTIFY_BULK_CREATE_SUBSCRIBERS_WITHOUT_PKS=True)
    def test_bulk_create_triggers_subscription(self):
        names = ["new-{v}".format(v=i) for i in range(100)]
        # Bulk create
        with self.assertLogs(log, level=logging.DEBUG) as cm:
            self.TestModel.objects.using(self.db_alias).bulk_create(
                [self.TestModel(name=name) for name in names]
            )

        self.assertEqual(
            cm.output,
            ["DEBUG:demo.subscription:Bulk Created {}".format(name) for name in names],
        )

    @override_settings(NOTIFY_BULK_CREATE_SUBSCRIBERS_WITHOUT_PKS=True)
    def test_bulk_create_triggers_subscription_and_returns_none_as_ids(self):
        connection = connections[self.db_alias]
        names = ["new-{v}".format(v=i) for i in range(100)]
        # Bulk create
        with self.assertLogs(log, level=logging.DEBUG) as cm:
            objs = self.TestModel.objects.using(self.db_alias).bulk_create(
                [self.TestModel(name=name) for name in names]
            )

        self.assertEqual(
            cm.output,
            ["DEBUG:demo.subscription:Bulk Created {}".format(name) for name in names],
        )

        if connection.features.can_return_ids_from_bulk_insert:
            for obj in objs:
                self.assertIsNot(obj.pk, None)
        else:
            self.assertEqual(
                [None for _ in range(len(names))], [obj.pk for obj in objs]
            )

    @override_settings(NOTIFY_BULK_CREATE_SUBSCRIBERS_WITHOUT_PKS=True)
    def test_bulk_update_triggers_subscription(self):
        connection = connections[self.db_alias]
        names = ["new-{v}".format(v=i) for i in range(100)]
        # Bulk create
        with self.assertLogs(log, level=logging.DEBUG) as cm:
            objs = self.TestModel.objects.using(self.db_alias).bulk_create(
                [self.TestModel(name=name) for name in names]
            )

        self.assertEqual(
            cm.output,
            ["DEBUG:demo.subscription:Bulk Created {}".format(name) for name in names],
        )
        new_name = "new"

        with self.assertLogs(log, level=logging.DEBUG) as cm:
            obj_pks = (
                [obj.pk for obj in objs]
                if connection.features.can_return_ids_from_bulk_insert
                else (
                    self.TestModel.objects.using(self.db_alias).values_list(
                        "pk", flat=True
                    )
                )
            )

            self.TestModel.objects.using(self.db_alias).filter(id__in=obj_pks).update(
                name=new_name
            )

        self.assertEqual(
            cm.output,
            [
                "DEBUG:demo.subscription:Bulk Updated {}".format(new_name)
                for _ in range(len(obj_pks))
            ],
        )

    @override_settings(NOTIFY_BULK_CREATE_SUBSCRIBERS_WITHOUT_PKS=True)
    def test_bulk_delete_triggers_subscription(self):
        connection = connections[self.db_alias]
        names = ["new-{v}".format(v=i) for i in range(100)]
        # Bulk create
        with self.assertLogs(log, level=logging.DEBUG) as cm:
            objs = self.TestModel.objects.using(self.db_alias).bulk_create(
                [self.TestModel(name=name) for name in names]
            )

        self.assertEqual(
            cm.output,
            ["DEBUG:demo.subscription:Bulk Created {}".format(name) for name in names],
        )

        with self.assertLogs(log, level=logging.DEBUG) as cm:
            obj_pks = (
                [obj.pk for obj in objs]
                if connection.features.can_return_ids_from_bulk_insert
                else (
                    self.TestModel.objects.using(self.db_alias).values_list(
                        "pk", flat=True
                    )
                )
            )

            self.TestModel.objects.using(self.db_alias).filter(id__in=obj_pks).delete()

        self.assertEqual(
            cm.output,
            ["DEBUG:demo.subscription:Bulk Deleted {}".format(name) for name in names],
        )


@override_settings(
    SUBSCRIPTION_MODULE="subscription",
    SUBSCRIPTION_AUTO_DISCOVER=False,
)
class ModelSubscriptionPostgresTransactionTestCase(
    ModelSubscriptionSqliteTransactionTestCase
):
    db_alias = "postgres"
    databases = {"postgres"}


@override_settings(
    SUBSCRIPTION_MODULE='subscription',
    SUBSCRIPTION_AUTO_DISCOVER=False,
)
class ModelSubscriptionMysqlTransactionTestCase(
    ModelSubscriptionSqliteTransactionTestCase
):
    db_alias = 'mysql'
    databases = {"mysql"}
