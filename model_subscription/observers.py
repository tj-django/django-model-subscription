import threading
from abc import ABC, abstractmethod
from typing import Callable, List, Tuple, Union, overload, NoReturn, Dict

from django.db import models

from model_subscription.constants import OperationType


class Observer(ABC):
    """
    The Observer interface declares the update method.
    """

    def __init__(self):
        self.lock = threading.Lock()
        self._receivers = (
            []
        )  # type: List[Tuple[int, Callable[[models.Model, Dict], NoReturn]]]

    @property
    @abstractmethod
    def action(self):
        pass

    @overload
    def handle(self, instances):
        # type: (List[models.Model]) -> None
        pass

    @abstractmethod  # noqa: F811
    def handle(self, instance, changed_data=None):
        # type: (models.Model, dict) -> None
        """
        Receive update from subject.
        """
        pass

    @property
    def receivers(self):
        return self._receivers

    @receivers.setter
    def receivers(self, other):
        # type: (Union[Callable, list]) -> None
        with self.lock:
            if isinstance(other, list):
                self._receivers = []
                for receiver in other:
                    if id(receiver) not in [x[0] for x in self._receivers]:
                        self._receivers.append((id(receiver), receiver))
            else:
                if id(other) not in [x[0] for x in self._receivers]:
                    self._receivers.append((id(other), other))


"""
Concrete Observers react to the operations issued by the Model they have been attached to.
"""


class CreateObserver(Observer):
    action = OperationType.CREATE

    def handle(self, instance, changed_data=None):
        # type: (models.Model, dict) -> None
        for _, receiver in self.receivers:
            receiver(instance)


class BulkObserverMixin(object):
    def handle(self, instances):
        # type: (List[models.Model]) -> None
        for _, receiver in self.receivers:
            receiver(instances)


class BulkCreateObserver(BulkObserverMixin, Observer):
    action = OperationType.BULK_CREATE


class BulkUpdateObserver(BulkObserverMixin, Observer):
    action = OperationType.BULK_UPDATE


class BulkDeleteObserver(BulkObserverMixin, Observer):
    # tyoe:
    action = OperationType.BULK_DELETE


class UpdateObserver(Observer):
    action = OperationType.UPDATE

    def handle(self, instance, changed_data=None):
        # type: (models.Model, dict) -> None
        for _, receiver in self.receivers:
            receiver(instance, changed_data)


class DeleteObserver(Observer):
    action = OperationType.DELETE

    def handle(self, instance, changed_data=None):
        # type: (models.Model, dict) -> None
        for _, receiver in self.receivers:
            receiver(instance)
