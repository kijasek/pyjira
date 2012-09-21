# -*- coding: utf8 -*-
from setuptools import setup, find_packages

setup(name='pyjira',
      version='0.1',
      packages=find_packages(),
      install_requires=['distribute', 'jira-python'],
      package_data={'pyjira': ['*.conf']},
      entry_points={
          'console_scripts': ['pyjira = pyjira.cli:main']
      },
      author='Tomasz Kijas',
      author_email='kijasek@gmail.com',
      description='CLI for JIRA to simplify daily tasks',
      url='https://github.com/kijasek/pyjira')
