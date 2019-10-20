from django.test import TestCase

# Create your tests here.
import os

import django
from django.conf import settings

# Create your tests here.

if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_model_subscription.settings'
    django.setup()

    from demo.models import TestModel


    t = TestModel.objects.create(name='test')
