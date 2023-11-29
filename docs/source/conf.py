# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os, sys
from configparser import ConfigParser
sys.path.insert(0, os.path.abspath("../../src"))

project = "graphab4py"
copyright = "2023, Manuel R. Popp"
author = "Manuel R. Popp"

# Read version from setup.py
with open(os.path.abspath("../../setup.py"), "r") as setup_file:
    lines = setup_file.readlines()
    for line in lines:
        if line.startswith("__version__"):
            release = line.split("=")[1].strip().strip('"').strip("'")
            break
    else:
        release = "unknown"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc"
]

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]

html_additional_pages = {
    "custom_singlehtml" : "layout.html",
}
