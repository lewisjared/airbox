"""
airbox

A set of utilities and a command line tool for managing AirBox and the
instruments in it.

Install using

    pip install airbox

Although it is likely to be only installed on one computer!

"""

from os.path import join, abspath, dirname
import os
from setuptools import setup, find_packages

root_dir = abspath(dirname(__file__))


with open(join(root_dir, "README.md"), "r") as f:
    readme = f.read()


setup(
    name="airbox",
    version=0.1,
    description="Set of helpers for managing AirBox",
    long_description=readme,
    author="Jared Lewis",
    author_email="jared.lewis@unimelb.edu.au",
    url="https://github.com/lewisjared/airbox",
    license="MIT",
    keywords=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=[],
        entry_points={
        'console_scripts':
            ['airbox = airbox.cli:main']
    },
)
