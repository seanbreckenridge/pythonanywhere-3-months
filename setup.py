#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("requirements.txt") as requirements_file:
    requirements = list(map(str.strip, requirements_file.read().splitlines()))

setup(
    author="Sean Breckenridge",
    author_email='seanbrecke@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    install_requires=requirements,
    license="Unlicense",
    include_package_data=True,
    name='pythonanywhere-3-months',
    packages=find_packages(include=['pythonanywhere_3_months']),
    entry_points = {
        'console_scripts': [
            "pythonanywhere_3_months = pythonanywhere_3_months.driver:main"
        ]
    },
    url='https://github.com/seanbreckenridge/pythonanywhere-3-months',
    version='0.1.0',
    zip_safe=True,
)
