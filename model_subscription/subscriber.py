from abc import ABC, abstractmethod
from typing import Callable, List, FrozenSet, Tuple, Type, Any, Optional, Union

from django.conf import settings
from django.db import models
from django.utils.module_loading import autodiscover_modules

from model_subscription.constants import OperationType
from model_subscription.observers import (
    Observer,
    CreateObserver,
    UpdateObserver,
    DeleteObserver,
    BulkCreateObserver,
    BulkUpdateObserver,
    BulkDeleteObserver,
)


class BaseSubscription(ABC):
    @abstractmethod
    def attach(self, operation_type, receiver):
        # type: (OperationType, Callable) -> None
        """
        Attach an observer.
        """
        pass

    @abstractmethod
    def detach(self, operation_type, receiver):
        # type: (OperationType, Callable) -> None
        """
        Detach an observer.
        """
        pass

    @abstractmethod
    def notify(self, operation_type, instance):
        # type: (OperationType, Type[models.Model]) -> None
        """
        Notify all observers about an event.
        """
        pass

    @abstractmethod
    def notify_many(self, operation_type, objs):
        # type: (OperationType.BULK_CREATE, List[models.Model]) -> None
        """
        Notify the observers of (bulk) actions.
        """
        pass


class ModelSubscription(BaseSubscription):
    """
    Notifies observers when the state changes.
    """

    def __init__(self):
        """
        Subscription types and List of subscribers.
        """
        self.__observers = frozenset(
            [
                (OperationType.CREATE, CreateObserver()),
                (OperationType.BULK_CREATE, BulkCreateObserver()),
                (OperationType.UPDATE, UpdateObserver()),
                (OperationType.BULK_UPDATE, BulkUpdateObserver()),
                (OperationType.DELETE, DeleteObserver()),
                (OperationType.BULK_DELETE, BulkDeleteObserver()),
            ]
        )  # type: FrozenSet[Tuple[OperationType, Observer]]

        self.__subscription_model = None  # type: Optional[models.Model]

    @property
    def observers(self):
        return dict(self._ModelSubscription__observers)

    @property
    def subscription_model(self):
        return self._ModelSubscription__subscription_model

    @subscription_model.setter
    def subscription_model(self, model):
        self._ModelSubscription__subscription_model = model

    def attach(self, operation_type, receiver):
        # type: (OperationType, Callable[[Any], Any]) -> None
        self.observers[operation_type].receivers = receiver

    def detach(self, operation_type, receiver):
        # type: (OperationType, Callable[[Any], Any]) -> None
        current_receivers = self.observers[operation_type].receivers
        self.observers[operation_type].receivers = [
            r[1] for r in current_receivers if r[0] != id(receiver)
        ]

    @staticmethod
    def auto_discover():
        autodiscover_modules(settings.SUBSCRIPTION_MODULE)

    def notify(self, operation_type, instance):
        # type: (Union[OperationType.CREATE, OperationType.UPDATE, OperationType.DELETE], Type[Any]) -> None
        self.subscription_model = instance
        observer = self.observers[operation_type]

        observer.handle(
            self.subscription_model,
            self.subscription_model._diff_with_initial,
        )

    def notify_many(self, operation_type, objs):
        # type: (Union[OperationType.BULK_CREATE, OperationType.BULK_UPDATE, OperationType.BULK_DELETE], List[models.Model]) -> None
        observer = self.observers[operation_type]  # type: BulkCreateObserver
        observer.handle(objs)
