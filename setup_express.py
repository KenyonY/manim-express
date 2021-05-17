#!/usr/bin/env python

from __future__ import print_function
from setuptools import setup, find_packages
from glob import glob
import manim_express as my_package

with open(glob('requirements.txt')[0], encoding='utf-8') as f:
    all_reqs = f.read().split('\n')
install_requires = [x.strip() for x in all_reqs]

with open("README.md", "r", encoding='utf-8') as fr:
    long_description = fr.read()

setup(name=my_package.__name__,
      version=my_package.__version__,
      package_data={
          'mainm_express': [
              '*.yaml', '*.yml',
          ],
      },
      description=" Animation engine for explanatory math videos",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author="K.y",
      author_email="beidongjiedeguang@gmail.com",
      url="https://github.com/beidongjiedeguang/mainm_express",
      license="MIT",
      install_requires=install_requires,
      classifiers=[
          'Operating System :: OS Independent',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.8",
      ],
      keywords=[
          'Computer Vision', 'Mathematics', 'Physics', 'Machine Learning', 'Neural Networks',
      ],
      packages=find_packages()
      )

