#!/usr/bin/env python

from __future__ import print_function
from setuptools import setup

pkgname = "manim_express"
pkgdir = pkgname

setup(
    setup_requires=['pbr>=1.9', 'setuptools>=17.1'],
    pbr=True,
    package_data={
        pkgdir: [
            '*.yaml', '*.yml',
        ],
    },
)
