# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = "mymath",
    packages = find_packages(),
    version = "0.1.0",
    install_requires=[
        "numpy",
        "scipy"
    ]
)