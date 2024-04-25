#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst', encoding="utf-8") as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst', encoding="utf-8") as history_file:
    history = history_file.read()

requirements = ['pm4py~=2.7.11.7',
                'textdistance~=4.6.1',
                'typing-extensions~=4.11.0',
                'numpy~=1.26.4',
                'matplotlib~=3.8.4',
                'static-frame~=2.6.0']

test_requirements = ['pytest>=3']

setup(
    author="Aaron F. Kurz",
    author_email='aaron.kurz@unisg.ch',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description=("Activity and Sequence Detection Performance Measures: A package to evaluate"
                 " activity detection results, including the sequence of events given multiple"
                 " activity types."),
    install_requires=requirements,
    license='GNU General Public License v3 or later (GPLv3+)',
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='aqudem',
    name='aqudem',
    packages=find_packages(include=['aqudem', 'aqudem.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/aaronkurz/aqudem',
    version='0.1.0',
    zip_safe=False,
)
