Subscriber Model
================

To enable observers that listen to model changes.

Update your django model by subclaassing SubscriptionModel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Swap ``models.Model`` with ``model_subscription.SubscriptionModel``
* This comes with it's own ``objects`` QuerySet manager.


**BEFORE**

.. code-block:: python

    from django.db import models


    class MyModel(models.Model):
        field_a = models.CharField(max_length=255)


**AFTER**

.. code-block:: python

    from moddel_subscripton import SubscriptionModel


    class MyModel(SubscriptionModel):
        field_a = models.CharField(max_length=255)


Alternatively if you don't want to subclass the ``SubscriptionModel`` see below.

Using the ``SubscriptionModelMixin`` and the ``SubscriptionQuerySet``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**BEFORE**

.. code-block:: python

    from django.db import models


    class MyModelQuerySet(models.QuerySet):

        def active(self):
            ...


    class MyModel(models.Model):
        field_a = models.CharField(max_length=255)

        objects = MyModelQuerySet.as_manager()


**AFTER**


.. code-block:: python

    from django.db import models

    from model_subscription.mixin import SubscriptionModelMixin
    from model_subscription.model import SubscriptionQuerySet


    class MyModelQuerySet(SubscriptionQuerySet):

        def active(self):
            ...


    class MyModel(SubscriptionModelMixin, models.Model):
        field_a = models.CharField(max_length=255)

        objects = MyModelQuerySet.as_manager()
