from setuptools import find_packages, setup


# Dynamically calculate the version based on model_subscription.VERSION.
version = __import__('model_subscription').__version__

install_requires = [
    'Django',
    'django-lifecycle>=0.3.0',
]
local_dev_requires = [
    'pip-tools==4.2.0',
    'check-manifest==0.40',
]

setup(
    name='django-model-subscription',
    author='Tonye Jack',
    version=version,
    description='Subscription model for a django model instance.',
    url='https://github.com/jackton1/django-model-subscription',
    install_requires=[
        'Django',
        'django-lifecycle>=0.3.0',
    ],
    extras_require={
      'development': local_dev_requires,
    }
)
