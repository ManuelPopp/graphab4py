#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remove TOC from documentation
"""
__author__ = "Manuel"
__date__ = "Wed Nov 29 15:39:49 2023"
__credits__ = ["Manuel R. Popp"]
__license__ = "Unlicense"
__version__ = "1.0.1"
__maintainer__ = "Manuel R. Popp"
__email__ = "requests@cdpopp.de"
__status__ = "Development"

#-----------------------------------------------------------------------------|
import os
dir_current = os.path.dirname(__file__)
dir_docs = os.path.dirname(dir_current)
file_path = os.path.join(dir_docs, "Graphab4Py.rst")

with open(file_path, "r", encoding = "utf-8") as f:
    lines = f.readlines()

drop = False
new_lines = []
for line in lines:
    if "indices-and-tables" in line:
        drop = True
    elif "module-graphab4py" in line:
        drop = False
    
    if not drop:
        new_lines += line

with open(file_path, "w") as file:
    file.writelines(new_lines)