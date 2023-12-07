#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Script name
-----------
test_graphab4py

Purpose
-------
Test the functions and the project class provided in graphab4py.

Notes
-----

'''

__author__ = "Manuel"
__date__ = "Wed Dec  6 18:27:32 2023"
__credits__ = ["Manuel R. Popp"]
__license__ = "Unlicense"
__version__ = "1.0.1"
__maintainer__ = "Manuel R. Popp"
__email__ = "requests@cdpopp.de"
__status__ = "Production"

#-----------------------------------------------------------------------------|
import os, unittest
from src.graphab4py import get_graphab

class TestGraphab4py(unittest.TestCase):
    def test_get_graphab(self):
        out_file, out_status = get_graphab()
        succeeded = os.path.isfile(out_file)
        
        self.assertEqual(succeeded, True)