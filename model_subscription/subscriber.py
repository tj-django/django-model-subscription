from abc import ABC, abstractmethod
from importlib import import_module
from typing import Set, Dict, Callable

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django_lifecycle import LifecycleModelMixin

from model_subscription.constants import OperationType
from model_subscription.observers import Observer, CreateObserver, UpdateObserver, DeleteObserver


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
    def notify(self, operation_type):
        # type: (OperationType) -> None
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
    _observers = {  # type: Dict[OperationType, Set[Observer]]
        OperationType.CREATE: CreateObserver(),
        OperationType.UPDATE: UpdateObserver(),
        OperationType.DELETE: DeleteObserver(),
    }

    """
    List of subscribers. In real life, the list of subscribers can be stored
    more comprehensively (categorized by event type, etc.).
    """

    @property
    def subscription_model(self):
        return self._subscription_model

    @subscription_model.setter
    def subscription_model(self, model):
        self._subscription_model = model

    def attach(self, operation_type, receiver):
        # type: (OperationType, Callable) -> None
        self._observers[operation_type].receivers = receiver

    def detach(self, operation_type, receiver):
        # type: (OperationType, Callable) -> None
        current_receivers = self._observers[operation_type].receivers
        del self._observers[operation_type].receivers
        self._observers[operation_type].receivers = [
            r[1] for r in current_receivers if r[0] != id(receiver)
        ]

    def auto_discover(self):
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

    def notify(self, operation_type):
        # type: (OperationType) -> None
        """
        Trigger an update in each subscriber.
        """
        observer = self._observers[operation_type]

        observer.handle(
            self.subscription_model,
            self.subscription_model._diff_with_initial,
        )
