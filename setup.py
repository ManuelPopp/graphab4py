#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 15:04:27 2023
"""
__author__ = "Manuel"
__date__ = "Tue Sep 26 15:04:27 2023"
__credits__ = ["Manuel R. Popp"]
__license__ = "Unlicense"
__version__ = "1.0.2"
__maintainer__ = "Manuel R. Popp"
__email__ = "requests@cdpopp.de"
__status__ = "Development"

#-----------------------------------------------------------------------------|
import os
from setuptools import setup, find_packages
dir_main = os.path.abspath(os.path.dirname(__file__))

setup(
      name = "graphab4py",
      version = "1.0.1b",
      author = "Manuel R. Popp",
      author_email = "requests@cdpopp.de",
      description = "A Python interface to Graphab.",
      long_description = open("README.rst").read(),
      install_requires = [
          "numpy", "matplotlib"
          ],
      package_dir = {"": "src"},
      packages = find_packages("./src"),
      classifiers = [
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: Unlicense",
          "Operating System :: OS Independent"
          ],
      python_requires = ">=3.9",
      url = "https://github.com/ManuelPopp/graphab4py",
      keywords = ["Graphab", "Network analysis"]
      )
