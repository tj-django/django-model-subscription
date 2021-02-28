import os
import io

from setuptools import find_packages, setup

BASE_DIR = os.path.dirname(__file__)
README_PATH = os.path.join(BASE_DIR, "README.md")
README_RST_PATH = os.path.join(BASE_DIR, "README.rst")

if os.path.isfile(README_PATH):
    with io.open(README_PATH, encoding="utf-8") as f:
        LONG_DESCRIPTION = f.read()
        LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'
else:
    with io.open(README_RST_PATH, encoding="utf-8") as f:
        LONG_DESCRIPTION = f.read()
        LONG_DESCRIPTION_CONTENT_TYPE = 'text/x-rst'

VERSION = (0, 2, 0)

version = ".".join(map(str, VERSION))

setup(
    name="django-model-subscription",
    version="0.0.10",
    description="Subscription model for a django model instance.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    python_requires="<4.0,>=3.4",
    project_urls={
        "documentation": "https://django-model-subscription.readthedocs.io/en/latest/index.html",
        "homepage": "https://django-model-subscription.readthedocs.io/en/latest/index.html",
        "repository": "https://github.com/jackton1/django-model-subscription",
    },
    author="Tonye Jack",
    author_email="tonyejck@gmail.com",
    license="MIT",
    zip_safe=False,
    keywords="django model subscription model observer model change subscriber model subscriptions model instance subscription",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    packages=find_packages(exclude=["django_model_subscription", "demo", "tests"]),
    install_requires=[
        "django-lifecycle==0.9.*,>=0.9.0",
        "six==1.*,>=1.14.0",
        'typing==3.*,>=3.6.0; python_version == "2.7.*" and python_version >= "2.7.0" or python_version == "3.4.*" and python_version >= "3.4.0"',
        "typing-extensions==3.*,>=3.7.0",
    ],
    extras_require={
        "deploy": [
            'bump2version==0.*,>=0.5.11; python_version == "2.*" and python_version >= "2.7.0" or python_version == "3.*" and python_version >= "3.5.0"',
            'git-changelog==0.*,>=0.1.0; python_version == "3.*" and python_version >= "3.6.0"',
        ],
        "dev": [
            'bump2version==0.*,>=0.5.11; python_version == "2.*" and python_version >= "2.7.0" or python_version == "3.*" and python_version >= "3.5.0"',
            'check-manifest==0.*,>=0.40.0; python_version == "2.*" and python_version >= "2.7.0" or python_version == "3.*" and python_version >= "3.5.0"',
            "django==2.*,>=2.0.0",
            'django-stubs==1.*,>=1.1.0; python_version == "3.*" and python_version >= "3.6.0"',
            'git-changelog==0.*,>=0.1.0; python_version == "3.*" and python_version >= "3.6.0"',
            "lockfile==0.*,>=0.12.2",
            'mypy==0.*,>=0.720.0; python_version == "3.*" and python_version >= "3.6.0"',
            'mysqlclient==1.4.4; python_version == "3.*" and python_version >= "3.6.0"',
            "poetry==1.1.0",
            'psycopg2==2.7.3.1; python_version == "2.7.*" or python_version == "3.4.*" or python_version == "3.5.*" or python_version == "3.6.*" or python_version == "3.7.*"',
            "recommonmark==0.*,>=0.6.0",
            "sphinx==1.8.5",
            "sphinx-autobuild==0.*,>=0.7.1",
            "sphinx-rtd-theme==0.*,>=0.4.3",
            "tox==3.*,>=3.14.0",
        ],
        "development": [
            'check-manifest==0.*,>=0.40.0; python_version == "2.*" and python_version >= "2.7.0" or python_version == "3.*" and python_version >= "3.5.0"',
            "django==2.*,>=2.0.0",
        ],
    },
)
