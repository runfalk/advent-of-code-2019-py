#!/usr/bin/env python
import os
import re

from setuptools import setup, find_packages

readme = None
with open("README.rst") as f:
    readme = f.read()

setup(
    name="aoc-2019-py",
    version="0.1.0",
    description=("Solutions for Advent of Code 2019 in Python"),
    long_description=readme,
    author="Andreas Runfalk",
    author_email="andreas@runfalk.se",
    license="MIT",
    url="https://github.com/runfalk/advent-of-code-2019-py",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[],
    extras_require={"dev": ["black", "pytest",],},
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={"console_scripts": ["aoc = aoc:main"]},
)
