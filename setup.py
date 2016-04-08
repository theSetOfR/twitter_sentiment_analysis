#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='twitter_sentiment_analysis',
    version='0.1.0',
    description="A simple program to run sentiment analysis on Twitter using a support vector machine.",
    long_description=readme + '\n\n' + history,
    author="Ravi-Shyam Patel",
    author_email='patelravishyam@gmail.com',
    url='https://github.com/theSetOfR/twitter_sentiment_analysis',
    packages=[
        'twitter_sentiment_analysis',
    ],
    package_dir={'twitter_sentiment_analysis':
                 'twitter_sentiment_analysis'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='twitter_sentiment_analysis',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
