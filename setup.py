#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

import gitpullerd

setup(name='gitpullerd',
    version=gitpullerd.__version__,
    packages=['gitpullerd'],
    scripts=['scripts/gitpullerd'],
)
