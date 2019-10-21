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

    # Create
    t = TestModel.objects.create(name='test')

    # Bulk create
    objs = TestModel.objects.bulk_create([
        TestModel(name='new-{v}'.format(v=i))
        for i in range(100)
    ])


    # Update
    t.name = "New name"
    t.save()

    TestModel.objects.filter(id__in=[t.pk] + [obj.pk for obj in objs]).update(name='you')
