#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
    'click<5.0',
    'docker-py>=1.3.1',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='dockem',
    version='0.1.0',
    description="Dockem intends to be a wrapper for Docker console commands. It aims to become the developer's friend.",
    long_description=readme + '\n\n' + history,
    author="e-mips",
    author_email='info@e-mips.com.ar',
    url='https://github.com/ssaid/dockem',
    packages=[
        'dockem',
    ],
    package_dir={'dockem':
                 'dockem'},
    entry_points={
        'console_scripts': [
            'dockem = dockem.cli:main',
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='dockem',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
