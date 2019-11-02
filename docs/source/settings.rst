Settings
========

`SUBSCRIPTION_MODULE`: Set the module or package name where auto-discover should look for
application level subscriptions (Defaults to 'subscription').

.. warning:: Ensure that the module is a submodule in the app.

`SUBSCRIPTION_AUTO_DISCOVER`:  Switch Auto discover (on/off).

.. warning:: With auto discovery on this would trigger subscriptions anywhere the model object is used
 from scripts to executing management commands.

Sample Settings
----------------

.. code-block:: python

    SUBSCRIPTION_MODULE = 'subscription' # This requires an app_name.subscription module/package
    SUBSCRIPTION_AUTO_DISCOVER = True  # Turns on auto discovery





Auto discovery
--------------
Most use case for subscribing to model events are specific to when the app is running similar to how
django signals work.

App.ready
~~~~~~~~~
Use the apps.ready for more control over which subscribers needs to be registered at runtime.

.. warning:: Ensure `SUBSCRIPTION_AUTO_DISCOVER` is set to False or omitted from the settings.

.. code-block:: python

    from django.apps import AppConfig

    class MyAppConfig(AppConfig):
        name = 'my_app'

        def ready(self):
            from my_app import subscription


Subscriber Model
----------------

To enable observers that can listen to model changes.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


* Swap your `models.Model` class with `model_subscription.SubscriptionModel`
* This comes with it's own `objects` QuerySet manager.


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


* Using the `SubscriptionModelMixin`
