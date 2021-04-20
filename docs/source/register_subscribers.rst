Register subscribers
====================

Most use case for subscribing to model events are specific to when the app is running similar to how
django signals work.

Using App.ready (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use the apps.ready for more control over which subscribers needs to be registered at runtime.

.. warning:: Ensure ``SUBSCRIPTION_AUTO_DISCOVER`` is set to False or omitted from the settings.

- Edit the `__init__.py` in your app setting the `default_app_config`.


.. code-block:: python

    default_app_config = 'my_app.apps.MyAppConfig'


- Edit `apps.py` module importing you subscription module.

.. code-block:: python

    from django.apps import AppConfig

    class MyAppConfig(AppConfig):
        name = 'my_app'

        def ready(self):
            from my_app import subscription



Using Auto Discovery
~~~~~~~~~~~~~~~~~~~~

Sample Settings
----------------

.. code-block:: python

    SUBSCRIPTION_MODULE = 'subscription' # This requires an app_name.subscription module/package
    SUBSCRIPTION_AUTO_DISCOVER = True  # Turns on auto discovery
