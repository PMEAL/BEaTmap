import os
import sys
from distutils.util import convert_path

from setuptools import setup, find_packages


sys.path.append(os.getcwd())

main = {}
ver_path = convert_path("beatmap/__init__.py")
with open(ver_path) as f:
    for line in f:
        if line.startswith("__version__"):
            exec(line, main)

setup(
    name="beatmap",
    description="A tool for determining the valid P/P0 range in BET isotherms",
    zip_safe=False,
    long_description_content_type='text/markdown',
    version=main["__version__"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    packages=find_packages("."),
    install_requires=[
        "matplotlib",
        "numpy",
        "pandas",
        "prettytable",
        "scipy",
        "seaborn",
    ],
    author="PMEAL Team",
    author_email="jgostick@uwaterloo.ca",
    url="http://pmeal.org",
    project_urls={
        "Documentation": "https://pmeal.github.io/beatmap/",
        "Source": "https://github.com/PMEAL/beatmap/",
        "Tracker": "https://github.com/PMEAL/beatmap/issues",
    },
)
