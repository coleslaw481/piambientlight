#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "argparse",
    "configparser",
    "Pillow"
]

test_requirements = [
    "argparse",
    "configparser",
    "Pillow"
]

setup(
    name='piambientlight',
    version='0.1.0',
    description="RasbAmbient light driver for Rasberry PI using PI Camera",
    long_description=readme + '\n\n' + history,
    author="Chris Churas",
    author_email='churas@gmail.com',
    url='https://github.com/coleslaw481/piambientlight',
    packages=[
        'piambientlight',
    ],
    package_dir={'piambientlight':
                 'piambientlight'},
    scripts=['piambientlight/piambientlight.py'],
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='piambientlight',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7'
    ],
    test_suite='tests',
    tests_require=test_requirements
)
