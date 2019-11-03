Subscriber Model
================

Enabling observers that listen to model changes.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


* Swap your ``models.Model`` class with ``model_subscription.SubscriptionModel``
* This comes with it's own ``objects`` QuerySet manager.


BEFORE

.. code-block:: python

    from django.db import models

    class MyModel(models.Model):
        field_a = models.CharField(max_length=255)


AFTER

.. code-block:: python

    from moddel_subscripton import SubscriptionModel

    class MyModel(SubscriptionModel):
        field_a = models.CharField(max_length=255)


* Using the ``SubscriptionModelMixin``
