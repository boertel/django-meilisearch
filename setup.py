import os
import re
from setuptools import setup

def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)

version=get_version('django_meilisearch')

setup(
    name="django-meilisearch",
    version=version,
    description="A Django app to wrap your django model to a meilisearch index",
    long_description=open('README.rst').read(),
    author="Benjamin Oertel",
    author_email="benjamin.oertel@gmail.com",
    url="https://boertel.github.io/django-meilisearch",
    license="BSD-3-Clause",
    include_package_data=True,
    packages=['django_meilisearch', 'django_meilisearch.management', 'django_meilisearch.management.commands'],
    install_requires=[
        "Django>=2.0",
        "meilisearch >= 0.13.0",
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ]
)
