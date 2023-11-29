.. role:: bash(code)
   :language: bash

.. role:: python(code)
   :language: python


.. image:: ./docs/img/Ga4Py.png
   :align: center
   :alt: Logo
   :width: 400px
   

----

.. image:: https://img.shields.io/pypi/v/graphab4py.svg
   :target: https://pypi.org/project/graphab4py/

.. image:: https://img.shields.io/pypi/pyversions/graphab4py.svg
   :target: https://pypi.org/project/graphab4py

.. _Supported Python Versions: https://pypi.org/project/graphab4py

.. image:: https://travis-ci.org/username/graphab4py.svg?branch=master
   :target: https://travis-ci.org/username/graphab4py

.. _Build Status: https://travis-ci.org/username/graphab4py

.. image:: https://img.shields.io/pypi/dm/graphab4py.svg?label=PyPI%20downloads
   :target: https://pypi.org/project/graphab4py

.. _PyPI Downloads: https://pypi.org/project/graphab4py

.. image:: https://img.shields.io/badge/license-UNLICENSE-green.svg
   :target: https://unlicense.org/

=====
About
=====
This package provides a Python interface to the program `Graphab <https://sourcesup.renater.fr/www/graphab/en/home.html/>`_.
The author(s) of this Python package are not developing Graphab.
Rather, Graphab is an independent software which provides a graphical user interface, as well as a command line interface.
Further information on Graphab can be found `here <https://sourcesup.renater.fr/www/graphab/en/home.html>`_.

Also view the `documentation <https://htmlpreview.github.io/?https://github.com/ManuelPopp/graphab4py/blob/main/docs/build/html/index.html>`_ of this Python package.

=============
Prerequisites
=============
In order to install and use Graphab4py, `Python <https://www.python.org>`_ >= 3.8 and `Java <https://www.java.com>`_ >= 8 are both required.
It is also recommended to have `pip <https://pip.pypa.io/en/stable/installation/>`_ available to install the `latest version <https://pypi.org/project/graphab4py/#history>`_ of Graphab4py.
Graphab is not required for installation. It can be installed through Graphab4py if missing. Alternatively, Graphab4py can be set up to use an existing Graphab Java executable.

============
Installation
============
Graphab4Py is available on `PyPI <https://pypi.org/project/graphab4py>`_. To install Graphab4Py, simply run the following line:

.. code-block:: console
   
   pip install graphab4py
   

========
Examples
========
With Graphab4py installed, we will now look at a few examples.

Creating a project
++++++++++++++++++
In the following, we will create a new Graphab project from scratch.

.. code-block:: python
   
   import graphab4py
   graphab4py.set_graphab("/home/rca/opt/")
   prj = graphab4py.Project()
   
   prj.create_project(
       name = "MyProject", patches = "/home/rca/dat/pat/Patches.tif",
       habitat = 1, directory = "/home/rca/prj"
       )
   
   prj.create_linkset(
       disttype = "cost",
       linkname = "L1",
       threshold = 100000,
       cost_raster = "/home/rca/dat/res/resistance_surface.tif"
       )
   
   prj.create_graph(graphname = "G1")
   
   prj.save()
   
In this example, Graphab has already been downloaded and saved to a folder named :bash:`/home/rca/opt/`.
In a first step, Graphab4py is pointed to this folder. ALternatively, the :python:`get_graphab()` function can be used to download Graphab to a specific location.
Subsequently, the project is initialized. Here, the project is given a name and a project folder is created. Moreover, a file containing habitat patches must be provided.
This file is a raster (e.g., a GeoTIFF \*.tif file) with values encoded as INT2S. (Graphab does not accept another format.) The value or values for habitat patches must also be provided.
Now, we create a linkset. The values allowed for :python:`disttype` are :python:`"euclid"` and :python:`"cost"`, which refer to euclidean distance and cumulated cost.
For a linkset based on euclidean distances, the :python:`cost_raster` argument is not used. When, instead, a resistance surface is used, it needs to be provided as a raster file, as indicated in the example.
Moreover, a threshold can be set, to limit the distance for which links are calculated. This may be necessary when dealing with large sets of habitat patches in order to limit computing time.
Finally, we create a graph and save the project.

Loading an existing project
+++++++++++++++++++++++++++
Graphab4py can load existing Graphab projects (\*.xml). However, it also has its own format (\*.g4p) to save and load projects.

.. code-block:: python
   
   import graphab4py
   prj = graphab4py.Project()
   prj.load_project_xml("/home/rca/prj/MyProject/MyProject.g4p")
   
   prj.enable_distance_conversion(
      save_plot = "/home/rca/out/Distance_conversion.png", max_euc = 2200
      )
   
   prj.convert_distance(500, regression = "log")
   
   out = prj.calculate_metric(metric = "EC", d = 1500, p = 0.05)
   ec = out["metric_value"]
   
In this example, we load a project from a Graphab4py project file. Subsequently, we use the linkset that we have created in the previous step to establish a relationship between euclidean and cost distance.
We can set limits to the euclidean distance considered for fitting the model, in order to fit the model to a relevant interval of our data.
When :python:`save_plot` is set to a valid path, a figure is created, so we can inspect the relationship and decide whether we want to use the respective regression mode.
By default, a linear regression is forced through zero. We decided that in our case, a log-log regression might give better results.
We can use the :python:`convert_distance` function directly to establish a relationship and return an estimation for a distance translation.
If no relationship for the given distance interval and regression model has established so far, the method will internally call :python:`enable_distance_conversion` and pass the required arguments.
Note that changing the distance interval will overwrite any previously fit model for the same linkset and model type.
In the last line, we calculate the metric "equivalent connectivity" (EC) for the entire graph. This metric requires additional parameters :python:`d` and :python:`p`.
Other metrics might not require additional parameters. A list of all the available metrics and their parameters and properties can be viewed in the original `Graphab manual <https://sourcesup.renater.fr/www/graphab/en/documentation.html>`_.

=======
License
=======
This is free and unencumbered software released into the public domain, as declared in the `LICENSE <https://github.com/ManuelPopp/graphab4py/blob/main/LICENSE>`_ file.
