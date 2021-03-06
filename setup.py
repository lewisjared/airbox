"""
airbox

A set of utilities and a command line tool for managing AirBox and the
instruments in it.

Although it is likely to be only installed on one computer!

"""

from os.path import join, abspath, dirname

from setuptools import setup, find_packages

from airbox import __version__

root_dir = abspath(dirname(__file__))

with open(join(root_dir, "README.rst"), "r") as f:
    readme = f.read()

setup(
    name="airbox",
    version=__version__,
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
    install_requires=[
        # "pandas",
        # "matplotlib"
    ],
    entry_points={
        'console_scripts':
            ['airbox = airbox.cli:main']
    },
)
