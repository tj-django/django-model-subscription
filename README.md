[![PyPI](https://img.shields.io/pypi/v/django-model-subscription)](https://pypi.org/project/django-model-subscription/) [![Actions Status](https://github.com/jackton1/django-model-subscription/workflows/django%20model%20subscription%20test./badge.svg)](https://github.com/jackton1/django-model-subscription/actions?query=workflow%3A"django+model+subscription+test.")
[![Documentation Status](https://readthedocs.org/projects/django-model-subscription/badge/?version=latest)](https://django-model-subscription.readthedocs.io/en/latest/?badge=latest)

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/353aa86af402423cbcd4e810bca664cc)](https://www.codacy.com/gh/tj-django/django-model-subscription/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=tj-django/django-model-subscription&amp;utm_campaign=Badge_Grade) [![Codacy Badge](https://app.codacy.com/project/badge/Coverage/353aa86af402423cbcd4e810bca664cc)](https://www.codacy.com/gh/tj-django/django-model-subscription/dashboard?utm_source=github.com&utm_medium=referral&utm_content=tj-django/django-model-subscription&utm_campaign=Badge_Coverage) [![codecov](https://codecov.io/gh/tj-django/django-model-subscription/branch/master/graph/badge.svg?token=P5X3FM234E)](https://codecov.io/gh/tj-django/django-model-subscription) [![PyPI - License](https://img.shields.io/pypi/l/django-model-subscription.svg)](https://github.com/jackton1/django-model-subscription/blob/master/LICENSE)

[![Total alerts](https://img.shields.io/lgtm/alerts/g/tj-django/django-model-subscription.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/tj-django/django-model-subscription/alerts/) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/tj-django/django-model-subscription.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/tj-django/django-model-subscription/context:python) 
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/tj-django/django-model-subscription/main.svg)](https://results.pre-commit.ci/latest/github/tj-django/django-model-subscription/main)


[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-model-subscription.svg)](https://pypi.org/project/django-model-subscription)
[![PyPI - Django Version](https://img.shields.io/pypi/djversions/django-model-subscription.svg)](https://docs.djangoproject.com/en/3.2/releases/)
[![Downloads](https://pepy.tech/badge/django-model-subscription)](https://pepy.tech/project/django-model-subscription)

# django-model-subscription

## Table of contents
* [Motivation](#Motivation)
* [Installation](#Installation)
* [Usage](#Usage)
  * [Decorators](#Decorators)
  * [Setup Subscribers using AppConfig.ready](#setup-subscribers-using-appconfigready-recomended)
  * [Setup Subscribers with auto discovery](#setup-subscribers-using-auto-discovery)
* [Credits](#credits)
* [Resources](#resources)


### Features

- Using Observer Pattern notify subscribers about changes to a django model.
- Decouple Business logic from Models.save
- Support for bulk actions (Not available using django signals.)
- Use noop subscribers when `settings.SUBSCRIPTION_DISABLE_SUBSCRIBERS` is `True`
  which prevents having to mock subscribers that call external services in testing, local development
  environments.
- Show changes to the instance after it has been updated i.e diff's the initial state and the
current state.

<img width="580" alt="Subscriber" src="https://user-images.githubusercontent.com/17484350/139741273-83cd6400-552e-419f-8cca-0f13caacf5aa.png">


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

##### Using the `SubscriptionModelMixin` and `SubscriptionQuerySet`

```py
from model_subscription.mixin import SubscriptionModelMixin
from model_subscription.model import SubscriptionQuerySet


class TestModel(SubscriptionModelMixin, models.Model):
    name = models.CharField(max_length=255)

    objects = SubscriptionQuerySet.as_manager()
```

##### Subclassing the `SubscriptionModel` base class.

```py
from model_subscription.model import SubscriptionModel


class TestModel(SubscriptionModel):
    name = models.CharField(max_length=255)

```

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

#### Credits
- [django-lifecycle](https://github.com/rsinger86/django-lifecycle)


If you feel generous and want to show some extra appreciation:

[![Buy me a coffee][buymeacoffee-shield]][buymeacoffee]

[buymeacoffee]: https://www.buymeacoffee.com/jackton1
[buymeacoffee-shield]: https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png


#### Resources
- https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Observer.html
- https://refactoring.guru/design-patterns/observer
- https://hackernoon.com/observer-vs-pub-sub-pattern-50d3b27f838c

### TODO's
- Supporting field level subscriptions.
- Support class based subscribers which implements `__call__`
- Extend to include custom OperationType.
- Add support for using a single class to manage multiple actions i.e MyClass.update, MyClass.create.
