#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 15:04:27 2023
"""
__author__ = "Manuel"
__date__ = "Tue Sep 26 15:04:27 2023"
__credits__ = ["Manuel R. Popp"]
__license__ = "Unlicense"
__version__ = "1.0.4"
__maintainer__ = "Manuel R. Popp"
__email__ = "requests@cdpopp.de"
__status__ = "Development"

#-----------------------------------------------------------------------------|
import os
from setuptools import setup, find_packages
dir_main = os.path.abspath(os.path.dirname(__file__))

setup(
      name = "graphab4py",
      version = __version__,
      author = "Manuel R. Popp",
      author_email = "requests@cdpopp.de",
      description = "A Python interface to Graphab.",
      long_description = """
      
      graphab4py - A Python interface to Graphab
      ==========================================
      
      Graphab4py provides a Python interface to Graphab, allowing users to perform
      network analysis and related tasks.
      
      Features:
      - Integration with Graphab algorithms
      - Network analysis tools
      - Visualization functions
      
      For more information, visit: https://github.com/ManuelPopp/graphab4py
      
      """,
      install_requires = [
          "numpy", "matplotlib", "xmltodict"
          ],
      package_dir = {"" : "src"},
      packages = find_packages("./src"),
      exclude_package_data={"": ["./docs/*"]},
      classifiers = [
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: Unlicense",
          "Operating System :: OS Independent"
          ],
      python_requires = ">=3.8",
      url = "https://github.com/ManuelPopp/graphab4py",
      keywords = ["Graphab", "Network analysis"]
      )
