==============================
graphab4py 1.0.4 documentation
==============================

.. container:: document

   .. container:: documentwrapper

      .. container:: bodywrapper

         .. container:: body

            .. container:: section
               :name: welcome-to-graphab4py

               .. rubric:: Welcome to
                  graphab4py!\ `¶ <#welcome-to-graphab4py>`__

               .. container:: toctree-wrapper compound

            .. container:: section
               :name: module-graphab4py

               .. rubric:: graphab4py
                  documentation\ `¶ <#module-graphab4py>`__
                  :name: graphab4py-documentation

               graphab4py - A Python interface to Graphab

               Graphab4py provides a Python interface to Graphab,
               allowing users to perform network analysis and related
               tasks.

               Features: - Integration with Graphab algorithms - Network
               analysis tools - Visualization functions

               For more information, visit:
               https://github.com/ManuelPopp/graphab4py

               graphab4py - A Python interface to Graphab

               Graphab4py provides a Python interface to Graphab,
               allowing users to perform network analysis and related
               tasks.

               Features: - Integration with Graphab algorithms - Network
               analysis tools - Visualization functions

               For more information, visit:
               https://github.com/ManuelPopp/graphab4py

               *class *\ graphab4py.project.DistanceConverter(\ *linkset_info*, *regression*, *lower_limit=None*, *upper_limit=None*\ )\ `¶ <#graphab4py.project.DistanceConverter>`__
                  Bases: ``object``

                  predict_cost(\ *x*\ )\ `¶ <#graphab4py.project.DistanceConverter.predict_cost>`__
                     Estimate cumulative cost for a given euclidean
                     distance “x”.

                     .. container:: section
                        :name: parameters

                        .. rubric:: Parameters\ `¶ <#parameters>`__

                        xnumeric
                           Euclidean distance.

                     .. container:: section
                        :name: returns

                        .. rubric:: Returns\ `¶ <#returns>`__

                        yfloat
                           Estimated cumulative cost.

                  save_plot(\ *file*\ )\ `¶ <#graphab4py.project.DistanceConverter.save_plot>`__
                     Save regression plot to file.

                     .. container:: section
                        :name: id1

                        .. rubric:: Parameters\ `¶ <#id1>`__
                           :name: parameters-1

                        filestr
                           Output file.

                     .. container:: section
                        :name: id2

                        .. rubric:: Returns\ `¶ <#id2>`__
                           :name: returns-1

                        None.

                  show_plot()\ `¶ <#graphab4py.project.DistanceConverter.show_plot>`__
                     Distplay regression plot.

                     .. container:: section
                        :name: id3

                        .. rubric:: Returns\ `¶ <#id3>`__
                           :name: returns-2

                        None.

               *class *\ graphab4py.project.Project\ `¶ <#graphab4py.project.Project>`__
                  Bases: ``object``

                  calculate_metric(\ *metric*, *linkset=None*, *graph=None*, *mtype='global'*, *\*\*metric_args*\ )\ `¶ <#graphab4py.project.Project.calculate_metric>`__
                     Calculate a global metric.

                     .. container:: section
                        :name: id4

                        .. rubric:: Parameters\ `¶ <#id4>`__
                           :name: parameters-2

                        projectstr
                           Path to a Graphab project .xml file.

                        linksetstr
                           Name of the linkset.

                        graphstr
                           Graph name.

                        metricstr
                           Metric name.

                        mtypestr {local, global}
                           Metric type.

                        param kwargs:
                           Metric paramneters; Additional Graphab
                           settings.

                     .. container:: section
                        :name: id5

                        .. rubric:: Returns\ `¶ <#id5>`__
                           :name: returns-3

                        outdict
                           A dictionary containing process output and
                           project name.

                  convert_distance(\ *x*, *linkset=None*, *regression='linzero'*, *show_plot=False*, *save_plot=False*, *min_euc=None*, *max_euc=None*\ )\ `¶ <#graphab4py.project.Project.convert_distance>`__
                     Estimate the cumulative cost along an euclidean
                     distance. If no euclid-to-cost relationship has
                     been established yet, the method first calls
                     enable_distance_conversion().

                     .. container:: section
                        :name: id6

                        .. rubric:: Parameters\ `¶ <#id6>`__
                           :name: parameters-3

                        xnumeric
                           Euclidean distance for which cumulative cost
                           is to be estimated.

                        linksetstr, optional
                           Name of the linkset to use. The default is
                           None.

                        regressionstr in {log, linear, linearzero}, optional
                           Regression type. One in log (log-log
                           regression), linear (simple linear
                           regression), or linorig (linear regression
                           forced through the origin). The default is
                           “linearzero”.

                        min_eucfloat, optional
                           Minimum euclidean distance to consider for
                           the regression.

                        max_eucfloat, optional
                           Maximum euclidean distance to consider for
                           the regression.

                     .. container:: section
                        :name: id7

                        .. rubric:: Returns\ `¶ <#id7>`__
                           :name: returns-4

                        costfloat
                           Estimated cumulative cost corresponding to an
                           euclidean distance of “x”.

                  create_graph(\ *graphname*, *linkset=None*, *nointra=True*, *threshold=None*, *\*\*ga_settings*\ )\ `¶ <#graphab4py.project.Project.create_graph>`__
                     Create a graph.

                     .. container:: section
                        :name: id8

                        .. rubric:: Parameters\ `¶ <#id8>`__
                           :name: parameters-4

                        graphnamestr
                           Graph name.

                        linksetstr
                           Name of the linkset. The default is None.

                        nointrabool, optional
                           Set the “nointra” option. The default is
                           True.

                        thresholdint, optional
                           Maximum distance or maximum accumulated cost
                           (depending on the type of distance). The
                           default is None.

                        param kwargs:
                           Additional Graphab settings.

                     .. container:: section
                        :name: id9

                        .. rubric:: Returns\ `¶ <#id9>`__
                           :name: returns-5

                        proc_outbytes
                           Process output.

                  create_linkset(\ *disttype*, *linkname*, *threshold*, *complete=True*, *cost_raster=None*, *\*\*ga_settings*\ )\ `¶ <#graphab4py.project.Project.create_linkset>`__
                     Create a linkset.

                     .. container:: section
                        :name: id10

                        .. rubric:: Parameters\ `¶ <#id10>`__
                           :name: parameters-5

                        projectstr
                           Path to a Graphab project .xml file.

                        disttypestr
                           Type of distance to use. Either “euclid” or
                           “cost”.

                        linknamestr
                           Name of the linkset.

                        thresholdint
                           Maximum distance or maximum accumulated cost
                           (depending on the type of distance).

                        completebool, optional
                           Whether to create a complete linkset. The
                           default is True.

                        cost_rasterstr, optional
                           Path to an external cost raster file (.tif).
                           The default is None.

                        param kwargs:
                           Additional Graphab settings.

                     .. container:: section
                        :name: id11

                        .. rubric:: Returns\ `¶ <#id11>`__
                           :name: returns-6

                        proc_outbytes
                           Process output.

                  create_project(\ *name*, *patches*, *habitat*, *nomerge=False*, *nodata=None*, *minarea=None*, *maxsize=None*, *connexity=8*, *directory=None*, *overwrite=False*, *\*\*ga_settings*\ )\ `¶ <#graphab4py.project.Project.create_project>`__
                     Create a Graphab project.

                     .. container:: section
                        :name: id12

                        .. rubric:: Parameters\ `¶ <#id12>`__
                           :name: parameters-6

                        namestr
                           Project name.

                        patchesstr
                           File path of the patches file. Patches must
                           be a raster containing values encoded as
                           INT2S.

                        habitatint
                           Integer(s) indicating habitat patches.

                        nomergebool, optional
                           DESCRIPTION. The default is False.

                        nodataint, optional
                           NoData value. The default is None.

                        minareaTYPE, optional
                           DESCRIPTION. The default is None.

                        maxsizeTYPE, optional
                           DESCRIPTION. The default is None.

                        connexityint in {4, 8}, optional
                           Consider the 4 or 8 neighbours when merging
                           pixels to patches. The default is 8.

                        directorystr, optional
                           Directory in which the project shall be
                           created. If set to none, the current working
                           directory is used. The default is None.

                        overwritebool, optional
                           Overwrite Graphab project if a project
                           already exists at the given location.

                        param kwargs:
                           Dictionary containing Graphab settings.

                     .. container:: section
                        :name: id13

                        .. rubric:: Returns\ `¶ <#id13>`__
                           :name: returns-7

                        outdict
                           A dictionary containing process output and
                           project name.

                  delta_by_item(\ *metric*, *linkset=None*, *graph=None*, *select=None*, *select_from_file=None*, *obj='patch'*, *mpi=False*, *\*\*metric_args*\ )\ `¶ <#graphab4py.project.Project.delta_by_item>`__
                     Calculate a global metric in delta mode on patches
                     or links depending on obj parameter for the
                     selected graph.

                     .. container:: section
                        :name: id14

                        .. rubric:: Parameters\ `¶ <#id14>`__
                           :name: parameters-7

                        projectstr
                           Path to a Graphab project .xml file.

                        linksetstr
                           Name of the linkset.

                        graphstr
                           Graph name.

                        metricstr
                           Metric name.

                        selectlist, optional
                           Restrict the calculation to items (patches or
                           links) listed by identifier. The default is
                           None.

                        select_from_filestr, optional
                           Restrict the calculations on items listed in
                           a .txt file. The file must contain one
                           identifier per line. The default is None.

                        objstr {patch, link}, optional
                           Type of objects to remove. The default is
                           “patch”.

                        mpibool, optional
                           Run in MPI mode (on cluster).

                        param kwargs:
                           Metric paramneters; Additional Graphab
                           settings.

                     .. container:: section
                        :name: id15

                        .. rubric:: Returns\ `¶ <#id15>`__
                           :name: returns-8

                        outdict
                           A dictionary containing process output and
                           project name.

                  enable_distance_conversion(\ *linkset=None*, *regression='linzero'*, *show_plot=False*, *save_plot=False*, *min_euc=None*, *max_euc=None*, *\*\*kwargs*\ )\ `¶ <#graphab4py.project.Project.enable_distance_conversion>`__
                     Establish a relationship between euclidean and cost
                     distance.

                     .. container:: section
                        :name: id16

                        .. rubric:: Parameters\ `¶ <#id16>`__
                           :name: parameters-8

                        linksetstr, optional
                           Name of the linkset to use. The default is
                           None.

                        regressionstr in {log, linear, linearzero}, optional
                           Regression type. One in log (log-log
                           regression), linear (simple linear
                           regression), or linorig (linear regression
                           forced through the origin). The default is
                           “linearzero”.

                        min_eucfloat, optional
                           Minimum euclidean distance to consider for
                           the regression.

                        max_eucfloat, optional
                           Maximum euclidean distance to consider for
                           the regression.

                     .. container:: section
                        :name: id17

                        .. rubric:: Returns\ `¶ <#id17>`__
                           :name: returns-9

                        None.

                  load_project(\ *project_file*, *\*\*ga_settings*\ )\ `¶ <#graphab4py.project.Project.load_project>`__
                     Load an existing Graphab or Graphab4py project.

                     .. container:: section
                        :name: id18

                        .. rubric:: Parameters\ `¶ <#id18>`__
                           :name: parameters-9

                        project_filestr
                           File path of the project file (either an .xml
                           or a .g4p file).

                     .. container:: section
                        :name: id19

                        .. rubric:: Returns\ `¶ <#id19>`__
                           :name: returns-10

                        None.

                  load_project_xml(\ *project_file*, *\*\*ga_settings*\ )\ `¶ <#graphab4py.project.Project.load_project_xml>`__
                     Load an existing Graphab project.

                     .. container:: section
                        :name: id20

                        .. rubric:: Parameters\ `¶ <#id20>`__
                           :name: parameters-10

                        project_filestr
                           File path of the project file (either an .xml
                           or a .g4p file).

                     .. container:: section
                        :name: id21

                        .. rubric:: Returns\ `¶ <#id21>`__
                           :name: returns-11

                        None.

                  save()\ `¶ <#graphab4py.project.Project.save>`__
                     Save current instance.

                     .. container:: section
                        :name: id22

                        .. rubric:: Returns\ `¶ <#id22>`__
                           :name: returns-12

                        None.

               graphab4py.project.get_graphab(\ *directory*\ )\ `¶ <#graphab4py.project.get_graphab>`__
                  Download the Graphab .jar file.

                  .. container:: section
                     :name: id23

                     .. rubric:: Parameters\ `¶ <#id23>`__
                        :name: parameters-11

                     pathstr
                        Directory in which to store the application.

                  .. container:: section
                     :name: id24

                     .. rubric:: Returns\ `¶ <#id24>`__
                        :name: returns-13

                     exit_statustuple
                        (Directory, HTTPMessage)

               graphab4py.project.set_graphab(\ *path*\ )\ `¶ <#graphab4py.project.set_graphab>`__
                  Set directory to Graphab. This approach will set the
                  Graphab path across sessions.

                  .. container:: section
                     :name: id25

                     .. rubric:: Parameters\ `¶ <#id25>`__
                        :name: parameters-12

                     pathstr
                        Graphab .jar file or directory containing
                        exactly one version of Graphab.

                  .. container:: section
                     :name: raises

                     .. rubric:: Raises\ `¶ <#raises>`__

                     Exception
                        Invalid path.

                  .. container:: section
                     :name: id26

                     .. rubric:: Returns\ `¶ <#id26>`__
                        :name: returns-14

                     None.

               graphab4py.project.set_java(\ *path*\ )\ `¶ <#graphab4py.project.set_java>`__
                  Set Java executable. This approach will set the Jaca
                  path across sessions.

                  .. container:: section
                     :name: id27

                     .. rubric:: Parameters\ `¶ <#id27>`__
                        :name: parameters-13

                     pathstr
                        Path or shortcut to Java executable.

                  .. container:: section
                     :name: id28

                     .. rubric:: Raises\ `¶ <#id28>`__
                        :name: raises-1

                     Exception
                        FileNotFoundError. Raises error if Python fails
                        to contact Java via subprocess and to return the
                        Java version.

                  .. container:: section
                     :name: id29

                     .. rubric:: Returns\ `¶ <#id29>`__
                        :name: returns-15

                     None.

               graphab4py.project.sigterm_handler(\ *signum*, *frame*\ )\ `¶ <#graphab4py.project.sigterm_handler>`__

               graphab4py.project.try_java(\ *java*\ )\ `¶ <#graphab4py.project.try_java>`__
                  Try to receive and print the Java version from the
                  given path or shortcut.

                  .. container:: section
                     :name: id30

                     .. rubric:: Parameters\ `¶ <#id30>`__
                        :name: parameters-14

                     javastr
                        Path or shortcut to Java executable.

                  .. container:: section
                     :name: id31

                     .. rubric:: Raises\ `¶ <#id31>`__
                        :name: raises-2

                     FileNotFoundError
                        Raises error if Python fails to contact Java via
                        subprocess and to return the Java version.

                  .. container:: section
                     :name: id32

                     .. rubric:: Returns\ `¶ <#id32>`__
                        :name: returns-16

                     None.

   .. container:: sphinxsidebar

      .. container:: sphinxsidebarwrapper

         .. rubric:: `graphab4py <#>`__
            :name: graphab4py
            :class: logo

         .. rubric:: Navigation
            :name: navigation

         .. container:: relations

            .. rubric:: Related Topics
               :name: related-topics

            -  `Documentation overview <#>`__

   .. container:: clearer

.. container:: footer

   ©2023, Manuel R. Popp. \| Powered by `Sphinx
   6.2.0 <http://sphinx-doc.org/>`__ & `Alabaster
   0.7.13 <https://github.com/bitprophet/alabaster>`__
