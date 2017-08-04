#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

import gitpullerd

setup(name='gitpullerd',
    version=gitpullerd.__version__,
    packages=['gitpullerd'],
    entry_points={
        'console_scripts': [
            'gitpullerd = gitpullerd.main:run',
        ],
    },
    install_requires=['lockfile==0.8', 'netaddr>=0.7.7', 'python-daemon==1.5.5',
            'GitPython==2.1.5', 'voluptuous==0.8.4'],
)
