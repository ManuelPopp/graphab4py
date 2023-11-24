=====
About
=====
This package provides a Python interface to the program `Graphab <https://sourcesup.renater.fr/www/graphab/en/home.html/>`_. The author(s) of this Python package are not developing Graphab.

============
Installation
============
Graphab4Py is available on `PyPI <https://pypi.org/project/graphab4py>`_. To install Graphab4Py, run the following line:

.. code-block:: console
   pip install graphab4py
   

=======
Example
=======
.. code-block:: python
   
   from graphab4py import project
   project.set_graphab("/home/rca/opt/")
   prj = project.Project()
   
   prj.create_project(
       name = "MyProject", patches = "/home/rca/dat/pat/Patches.tif", habitat = 1, directory = "/home/rca/prj"
       )
   
   prj.create_linkset(
       disttype = "cost",
       linkname = "L1",
       threshold = 1000,
       cost_raster = "/home/rca/dat/res/resistance_surface.tif"
       )

   prj.create_graph(graphname = "G1")
   
===
End
===
