Settings
========

``SUBSCRIPTION_MODULE``: Set the module or package name where auto-discovery should look for
application level subscriptions (Defaults to ``subscription``).

.. warning:: Ensure that ``subscription`` module is a submodule of your app.

``SUBSCRIPTION_AUTO_DISCOVER``:  Toggle Auto discovery on/off (Defaults to ``False``).

.. warning:: With auto discovery on this would trigger subscriptions anywhere the model object is used
 from scripts to executing management commands.

``NOTIFY_BULK_CREATE_SUBSCRIBERS_WITHOUT_PKS``: Notify Bulk create subscribers when the database
 doesn't support returning id's for bulk inserts. (Defaults: ``connection.features.can_return_ids_from_bulk_insert``)


.. warning:: Note if set to ``True``, this would return the same objects passed to bulk create so
 accessing the ``pk`` or ``id`` field would return ``None``, if your database backend doesn't support
 returning id's for bulk inserts.
