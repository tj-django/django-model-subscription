from abc import ABC, abstractmethod
from importlib import import_module
from typing import Set, Dict, Callable, List

from django.conf import settings
from django.db import models
from django_lifecycle import LifecycleModelMixin

from model_subscription.constants import OperationType
from model_subscription.observers import (
    Observer, CreateObserver, UpdateObserver, DeleteObserver,
    BulkCreateObserver, BulkUpdateObserver, BulkDeleteObserver
)


class BaseSubscription(ABC):
    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    @abstractmethod
    def attach(self, operation_type, receiver):
        # type: (OperationType, Callable) -> None
        """
        Attach an observer to the subject.
        """
        pass

    @abstractmethod
    def detach(self, operation_type, receiver):
        # type: (OperationType, Callable) -> None
        """
        Detach an observer from the subject.
        """
        pass

    @abstractmethod
    def notify(self, operation_type, instance):
        # type: (OperationType, type(models.Model)) -> None
        """
        Notify all observers about an event.
        """
        pass


class ModelSubscription(BaseSubscription):
    """
    The Subject owns some important state and notifies observers when the state
    changes.
    """
    _subscription_model = None  # type: (LifecycleModelMixin, models.Model)
    _observers = frozenset(  # type: Set[OperationType, Set[Observer]]
        [
            (OperationType.CREATE, CreateObserver()),
            (OperationType.BULK_CREATE, BulkCreateObserver()),
            (OperationType.UPDATE, UpdateObserver()),
            (OperationType.BULK_UPDATE, BulkUpdateObserver()),
            (OperationType.DELETE, DeleteObserver()),
            (OperationType.BULK_DELETE, BulkDeleteObserver()),
        ]
    )

    """
    List of subscribers. In real life, the list of subscribers can be stored
    more comprehensively (categorized by event type, etc.).
    """

    @property
    def observers(self):
        return dict(self._observers)

    @property
    def subscription_model(self):
        return self._subscription_model

    @subscription_model.setter
    def subscription_model(self, model):
        self._subscription_model = model

    def attach(self, operation_type, receiver):
        # type: (OperationType, Callable) -> None
        self.observers[operation_type].receivers = receiver

    def detach(self, operation_type, receiver):
        # type: (OperationType, Callable) -> None
        current_receivers = self.observers[operation_type].receivers
        self.observers[operation_type].receivers = [
            r[1] for r in current_receivers if r[0] != id(receiver)
        ]

    @staticmethod
    def auto_discover():
        from django.apps import apps
        for app_config in apps.get_app_configs():
            app_name = app_config.name
            try:
                import_module(
                    '%(app_name)s.%(module_name)s' %
                    {
                        'app_name': app_name,
                        'module_name': settings.SUBSCRIPTION_MODULE
                    }
                )
            except ImportError:
                pass

    def notify(self, operation_type, instance):
        # type: (OperationType, type(models.Model)) -> None
        """
        Trigger an handles of the subscribers.
        """
        self.subscription_model = instance
        observer = self.observers[operation_type]

        observer.handle(
            self.subscription_model,
            self.subscription_model._diff_with_initial,
        )

    def notify_many(self, operation_type, objs):
        # type: (OperationType.BULK_CREATE, List[models.Model]) -> None
        observer = self.observers[operation_type]  # type: BulkCreateObserver
        observer.handle(objs)
