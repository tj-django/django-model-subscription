[![CircleCI](https://circleci.com/gh/tj-django/django-model-subscription.svg?style=shield)](https://circleci.com/gh/tj-django/django-model-subscription)
[![Actions Status](https://github.com/jackton1/django-model-subscription/workflows/django%20model%20subscription%20test./badge.svg)](https://github.com/jackton1/django-model-subscription/actions?query=workflow%3A"django+model+subscription+test.")
[![Documentation Status](https://readthedocs.org/projects/django-model-subscription/badge/?version=latest)](https://django-model-subscription.readthedocs.io/en/latest/?badge=latest)
[![PyPI - License](https://img.shields.io/pypi/l/django-model-subscription.svg)](https://github.com/jackton1/django-model-subscription/blob/master/LICENSE)

[![Total alerts](https://img.shields.io/lgtm/alerts/g/tj-django/django-model-subscription.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/tj-django/django-model-subscription/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/tj-django/django-model-subscription.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/tj-django/django-model-subscription/context:python)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-model-subscription.svg)](https://pypi.org/project/django-model-subscription)
[![PyPI - Django Version](https://img.shields.io/pypi/djversions/django-model-subscription.svg)](https://docs.djangoproject.com/en/2.2/releases/)
[![Downloads](https://pepy.tech/badge/django-model-subscription)](https://pepy.tech/project/django-model-subscription)

# [django-model-subscription](https://django-model-subscription.readthedocs.io/en/latest/installation.html)

![Sreenshot](https://media.giphy.com/media/IgvrR33L6S7nFgH1by/giphy.gif)


## Table of contents
* [Motivation](#Motivation)
* [Installation](#Installation)
* [Usage](#Usage)
* [Decorators](#Decorators)
* [Setup Subscribers using AppConfig.ready](#setup-subscribers-using-appconfigready-recomended)
* [Setup Subscribers with auto discovery](#setup-subscribers-using-auto-discovery)


### Motivation

- Using Observer Pattern notify subscribers about changes to a django model.
- Decouple Business logic from Models.save
- Support for bulk actions (Not available using django signals.)
- Use noop subscribers when `settings.SUBSCRIPTION_RUN_EXTERNAL` is `False` 
  which prevents having to mock subscribers that call external services in testing, local development 
  environments.
- Show changes to the instance after it has been updated i.e diff's the initial state and the 
current state.

![Screenshot](Subscriber.png)


### Installation

```bash
$ pip install django-model-subscription
```

Add `model_subscription` to your INSTALLED_APPS

```python
INSTALLED_APPS = [
    ...,
    'model_subscription',
    ...
]
```




### Usage

#### Creating subscribers.

- Using `OperationType`

```python
import logging
from model_subscription.decorators import subscribe
from model_subscription.constants import OperationType

log = logging.getLogger(__name__)

@subscribe(OperationType.CREATE, TestModel)
def handle_create(instance):
    log.debug('Created {}'.format(instance.name))


```

- Using `create_subscription` directly (succinct version).

```python

import logging
from model_subscription.decorators import create_subscription

log = logging.getLogger(__name__)

@create_subscription(TestModel)
def handle_create(instance):
    log.debug('Created {}'.format(instance.name))


```


### Decorators

* `subscribe`: Explicit (Requires a valid OperationType).


#### (Create, Update, Delete) operations. 

* `create_subscription`: Subscribes to create operation i.e a new instance.

```python
@create_subscription(TestModel)
def handle_create(instance):
    log.debug('1. Created {}'.format(instance.name))
```

* `update_subscription`: Subscribes to updates also includes (`changed_data`).
```python
@update_subscription(TestModel)
def handle_update(instance, changed_data):
    log.debug('Updated {} {}'.format(instance.name, changed_data))
```


* `delete_subscription`: Subscribes to delete operation: 

> NOTE: The instance.pk is already set to None.

```python
@delete_subscription(TestModel)
def handle_delete(instance):
    log.debug('Deleted {}'.format(instance.name))
```

#### (Bulk Create, Bulk Update, Bulk Delete) operations. 

* `bulk_create_subscription`: Subscribe to bulk create operations.

```python

@bulk_create_subscription(TestModel)
def handle_bulk_create(instances):
    for instance in instances:
        log.debug('Bulk Created {}'.format(instance.name))

```


* `bulk_update_subscription`: Subscribe to bulk update operations.

```python
@bulk_update_subscription(TestModel)
def handle_bulk_update(instances):
    for instance in instances:
        log.debug('Updated {}'.format(instance.name))
```


* `bulk_delete_subscription`: Subscribe to bulk delete operations.

```python

@bulk_delete_subscription(TestModel)
def handle_bulk_delete(instances):
    for instance in instances:
        log.debug('Deleted {}'.format(instance.name))

```


### Setup Subscribers using AppConfig.ready `(Recomended)`. 


Update you `apps.py`


```python

from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = 'myapp'

    def ready(self):
        from myapp import subscriptions

```



### Setup Subscribers using auto discovery.

By default the `settings.SUBSCRIPTION_AUTO_DISCOVER` is set to `False`.

To use auto discovery this is not recommended as it would notify the subscribers 
wherever the model is used i.e IPython notebook, external scripts.

In your `settings.py` add

```python

SUBSCRIPTION_AUTO_DISCOVER = True

```

#### Setting up the `SUBSCRIPTION_MODULE`

> NOTE: This is only required when ``SUBSCRIPTION_AUTO_DISCOVER = True``

```python

SUBSCRIPTION_MODULE  = 'subscription' 

```

#### Resources
- https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Observer.html
- https://refactoring.guru/design-patterns/observer
- https://hackernoon.com/observer-vs-pub-sub-pattern-50d3b27f838c

TODO's
- Supporting field level subscriptions.
- Support class based subscribers which implements `__call__`
- Extend to include custom OperationType.
- Add support for using a single class to manage multiple actions i.e MyClass.update, MyClass.create.
