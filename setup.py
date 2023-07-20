#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(name='update_was_targets',
      version='0.1.0',
      description='Updated WAS Targets based on tagged assets.',
      author='Andy Groome',
      packages=find_packages(),
      install_requires=[
          'pyTenable',
          'python-dotenv',
      ]
     )
