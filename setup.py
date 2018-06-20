#!/usr/bin/env python
from setuptools import setup

setup(
    name='discourse2fedmsg',
    description='discourse2fedmsg bridges discourse to fedmsg',
    version='0.1',
    author='Ralph Bean, Patrick Uiterwijk',
    author_email='rbean@redhat.com, puiterwijk@redhat.com',
    license='GPLv2+',
    url='https://pagure.io/discourse2fedmsg',
    py_modules=['discourse2fedmsg'],
    packages=[],
    install_requires=['fedmsg', 'flask'],

