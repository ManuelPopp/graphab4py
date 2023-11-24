#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 13:51:41 2023
"""
__author__ = "Manuel"
__date__ = "Mon Sep 25 13:51:41 2023"
__credits__ = ["Manuel R. Popp"]
__license__ = "Unlicense"
__version__ = "1.0.1"
__maintainer__ = "Manuel R. Popp"
__email__ = "requests@cdpopp.de"
__status__ = "Development"

#-----------------------------------------------------------------------------|
import os, sys, glob, platform, subprocess, signal, warnings
from urllib.request import urlretrieve

java = "/usr/bin/java" if platform.system() == "Linux" else "java"

try:
    ga_settings = {"java" : java,
                   "memory" : None,
                   "cores" : None,
                   "graphab" : None
                   }

except:
    ga_settings = {"java" : None,
                   "memory" : None,
                   "cores" : None,
                   "graphab" : None
                   }
    
    warnings.warn(
        " ".join(
            ["Unable to locate Java. Please set path to Java manually." +
             "To do so, assign the path to graphab4py.ga_settings['java']."]
            )
        )

process_ids = []

def sigterm_handler(signum, frame):
    print("Process will be terminated. Cleaning up...")
    for pid in process_ids:
        os.kill(pid, signal.SIGTERM)
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)

#-----------------------------------------------------------------------------|
# Functions
def set_graphab(path):
    '''
    Set directory to Graphab.
    
    Parameters
    ----------
    path : str
        Graphab *.jar file or directory containing exactly one version of
        Graphab.
    
    Raises
    ------
    Exception
        Invalid path.
    
    Returns
    -------
    None.
    '''
    if not isinstance(path, str):
        
        raise Exception(f"Invalid parameter {path}. Expected string.")
    
    if not (os.path.isdir(path) or os.path.isfile(path)):
        path = os.path.join(os.getcwd(), path)
    
    if os.path.isdir(path):
        ga_file = glob.glob(os.path.join(path, "graphab*.jar"))
        
        if len(ga_file) > 1:
            mssg = "Failed to locate Graphab (ambigious directory {0}) " + \
                "contains multiple files matching the pattern 'graphab*.jar'."
            
            raise Exception(mssg.format(path))
        
        elif len(ga_file) < 1:
            mssg = f"Failed to locate Graphab within {ga_file}."
            
            raise Exception(mssg)
    
    elif os.path.isfile(path):
        if os.path.splitext(path)[1] != ".jar":
            
            raise Exception("Graphab file must be a *.jar file.")
    
    else:
        raise Exception(f"No such file or directory: {path}.")
    
    global ga_settings
    ga_settings["graphab"] = path
    
    return

def get_graphab(directory):
    '''
    Download the Graphab *.jar file.
    
    Parameters
    ----------
    path : str
        Directory in which to store the application.
    
    Returns
    -------
    exit_status : tuple
        (Directory, HTTPMessage)
    '''
    if not (os.path.isdir(directory) or directory.endswith(".jar")):
        raise FileNotFoundError(
            f"{directory} is not a directory or valid file name."
            )
    
    filename = directory if directory.endswith(".jar") else os.path.join(
        directory, "Graphab-2.8.jar"
        )
    
    url = "https://thema.univ-fcomte.fr/productions/download.php?name=graphab&version=2.8&username=Graph4lg&institution=R"
    exit_status = urlretrieve(url, filename)
    
    set_graphab(filename)
    
    return exit_status

def base_call(java = None, memory = None, cores = None, graphab = None,
              **kwargs):
    '''
    Create and run a call to Graphab.
    
    Parameters
    ----------
    java : str, optional
        Path to the Java executable. The default is None.
    memory : str, optional
        Limit for RAM allocated by Graphab. Consists of number and unit.
        The default is None.
    cores : int, optional
        Number of CPU cores to provide to Graphab. The default is None.
    graphab : str, optional
        Path to the Graphab *.jar file. The default is None.
    **kwargs : dict, any
        Arguments to append to the Graphab call.
    
    Returns
    -------
    proc_out : bytes
        Process output.
    '''
    global ga_settings
    current_settings = ga_settings
    
    settings = {key : val for key, val in locals().items() if val is not None}
    
    if len(settings) > 0:
        current_settings.update(settings)
    
    java = current_settings["java"]
    graphab = current_settings["graphab"]
    
    if "mpi" in kwargs.keys():
        mpi = kwargs["mpi"]
        del kwargs["mpi"]
        
    else:
        mpi = False
    
    if mpi:
        cmd = ["mpirun", java, "-jar", graphab, "-mpi"]
    
    else:
        if current_settings["memory"] is not None:
            memory = current_settings["memory"]
            mem = [f"-Xmx{memory}"]
        else:
            mem = []
        
        cmd = [
            java, "-Djava.awt.headless=true"
            ] + mem + [
            "-jar", graphab
            ]
    
    if current_settings["cores"] is not None:
        cmd += ["-proc", str(current_settings["cores"])]
    
    for key, val in kwargs.items():
        values = val if isinstance(val, list) else [val]
        cmd += ["--{0}".format(key)] + values
    
    print("Running: {}".format(" ".join(cmd)))
    
    #proc_out = subprocess.check_output(cmd)
    process = subprocess.Popen(
        cmd,
        shell = False,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
        )
    pid = process.pid
    print(f"Started subprocess\nProcess ID: {pid}")
    
    global process_ids
    process_ids.append(pid)
    
    proc_out, proc_err = process.communicate()
    process_ids.pop()
    
    return proc_out

def create_project(name,
                   patches,
                   habitat,
                   nomerge = False,
                   nodata = None,
                   minarea = None,
                   maxsize = None,
                   connexity = 8,
                   directory = None,
                   **gasettings
                   ):
    '''
    Create a Graphab project.
    
    Parameters
    ----------
    name : str
        Name of the project.
    patches : str
        File path to the landscape raster.
    habitat : int
        Integer encoding the habitat type in the landscape raster.
    nomerge : bool, optional
        Whether not tomerge contiguous patches of dierent codes.
        The default is False.
    nodata : int, optional
        Code for NoData values. The default is None.
    minarea : int, optional
        Minimum patch size in ha. The default is None.
    maxsize : int, optional
        Max size in ha. Patches with an area exceeding maxsize will be split.
        The default is None.
    connexity : int in {4, 8}, optional
        Neighbourhood or 4 or 8 pixels in patch definition. The default is 4.
    directory : str, optional
        Directory into which the project is to be created. The default is None.
    **gasettings : dict
        Dictionary containing Graphab settings.
    
    Returns
    -------
    out : dict
        A dictionary containing process output and project name.
    '''
    directory = os.getcwd() if directory is None else directory
    
    project_settings = [name,
                        patches,
                        f"habitat={habitat}",
                        f"dir={directory}"
                        ]
    
    if nomerge:
        project_settings += ["nomerge"]
    
    if isinstance(nodata, int):
        project_settings += [f"nodata={nodata}"]
    
    if isinstance(minarea, int):
        project_settings += [f"minarea={minarea}"]
    
    if isinstance(maxsize, int):
        project_settings += [f"maxsize={maxsize}"]
    
    if connexity == 8:
        project_settings += ["con8"]
    
    proc_out = base_call(**ga_settings, create = project_settings)
    
    out = {"process_output" : proc_out,
           "project_file" : os.path.join(directory, name, name + ".xml")
           }
    
    return out

def create_linkset(project, disttype, linkname, threshold, complete = True,
                   cost_raster = None, **ga_settings):
    '''
    Create a linkset.
    
    Parameters
    ----------
    project : str
        Path to a Graphab project .xml file.
    disttype : str
        Type of distance to use. Either "euclid" or "cost".
    linkname : str
        Name of the linkset.
    threshold : int
        Maximum distance or maximum accumulated cost (depending on the type of
        distance).
    complete : bool, optional
        Whether to create a complete linkset. The default is True.
    cost_raster : str, optional
        Path to an external cost raster file (*.tif). The default is None.
    **ga_settings : any
        Additional Graphab settings.
    
    Returns
    -------
    proc_out : bytes
        Process output.
    '''
    link_settings = [f"distance={disttype}", f"name={linkname}"]
    
    if complete:
        link_settings += ["complete"]
    
    link_settings += [f"maxcost={threshold}"]
    
    if cost_raster is not None:
        link_settings += [f"extcost={cost_raster}"]
    
    proc_out = base_call(**ga_settings, project = project,
                         linkset = link_settings)
    
    return proc_out

def create_graph(graphname, project, linkset, nointra = True,
                 threshold = None, **ga_settings):
    '''
    Create a graph.
    
    Parameters
    ----------
    graphname : str
        Graph name.
    project : str
        Path to a Graphab project .xml file.
    linkset : str
        Name of the linkset.
    nointra : bool, optional
        Set the "nointra" option. The default is True.
    threshold : int, optional
        Maximum distance or maximum accumulated cost (depending on the type of
        distance). The default is None.
    **ga_settings : any
        Additional Graphab settings.
    
    Returns
    -------
    proc_out : bytes
        Process output.
    '''
    graph_settings = [f"name={graphname}"]
    
    if nointra:
        graph_settings += ["nointra"]
    
    if threshold is not None:
        graph_settings += [f"threshold={threshold}"]
    
    proc_out = base_call(**ga_settings, project = project,
                         uselinkset = linkset, graph = graph_settings)
    
    return proc_out

def calculate_metric(project, linkset, graph, metric, mtype = "global",
                     **metric_args):
    '''
    Calculate a global metric.
    
    Parameters
    ----------
    project : str
        Path to a Graphab project .xml file.
    linkset : str
        Name of the linkset.
    graph : str
        Graph name.
    metric : str
        Metric name.
    mtype : str {local, global}
        Metric type.
    **metric_args : dict
        Metric paramneters.
    **ga_settings : any
        Additional Graphab settings.
    
    Returns
    -------
    out : dict
        A dictionary containing process output and project name.
    '''
    metric_settings = [metric]
    ga_settings = {}
    
    for key, val in metric_args.items():
        if key in ["java", "memory", "cores", "graphab"]:
            ga_settings.update({key : val})
        
        else:
            metric_settings += ["{0}={1}".format(key, val)]
    
    match mtype:
        case "global":
            metric = {"gmetric" : metric_settings}
        
        case "component":
            metric = {"cmetric" : metric_settings}
        
        case "local":
            metric = {"lmetric" : metric_settings}
        
        case _:
            raise Exception(f"Illegal argument for mtype: {mtype}.")
    
    proc_out = base_call(**ga_settings, project = project,
                         uselinkset = linkset, usegraph = graph,
                         **metric)
    
    try:
        out_text = proc_out.decode("utf-8")
        
        metric_value = float(out_text.split(" ")[-1].strip())
        
        out = {"process_output" : proc_out,
               "metric_value" : metric_value}
    
    except:
        out = proc_out.decode("utf-8")
    
    return out

def delta_by_item(project, linkset, graph, metric, select = None,
                select_from_file = None, obj = "patch", mpi = False,
                **metric_args):
    '''
    Calculate a global metric in delta mode on patches or links depending on
    obj parameter for the selected graph.
    
    Parameters
    ----------
    project : str
        Path to a Graphab project .xml file.
    linkset : str
        Name of the linkset.
    graph : str
        Graph name.
    metric : str
        Metric name.
    select : list, optional
        Restrict the calculation to items (patches or links) listed by
        identifier. The default is None.
    select_from_file : str, optional
        Restrict the calculations on items listed in a *.txt file. The file
        must contain one identifier per line. The default is None.
    obj : str {patch, link}, optional
        Type of objects to remove. The default is "patch".
    mpi : bool, optional
        Run in MPI mode (on cluster).
    **metric_args : dict
        Metric paramneters.
    **ga_settings : any
        Additional Graphab settings.
    
    Returns
    -------
    out : dict
        A dictionary containing process output and project name.
    '''
    delta_settings = [metric]
    ga_settings = {}
    
    for key, val in metric_args.items():
        if key in ["java", "memory", "cores", "graphab"]:
            ga_settings.update({key : val})
        
        else:
            delta_settings += ["{0}={1}".format(key, val)]
    
    if select is not None:
        delta_settings += ["sel=" + ",".join(select)]
    
    if select_from_file is not None:
        delta_settings += [f"fsel={select_from_file}"]
    
    delta_settings += [f"obj={obj}"]
    
    proc_out = base_call(**ga_settings, project = project,
                         uselinkset = linkset, usegraph = graph, mpi = mpi,
                         delta = delta_settings)
    
    return proc_out

#-----------------------------------------------------------------------------|
# Classes
class Project():
    def __init__(self,
                 name,
                 patches,
                 habitat,
                 nomerge = False,
                 nodata = None,
                 minarea = None,
                 maxsize = None,
                 connexity = 8,
                 directory = None
                 ):
        self.name = name
        self.patches = patches
        self.habitat = habitat
        self.nomerge = nomerge
        self.minarea = minarea
        self.maxsize = maxsize
        self.connexity = connexity
        self.directory = directory if directory is not None else os.getcwd()
        self.project_file = os.path.join(directory, name, name + ".xml")
        self.linksets = None
        self.graphs = None
        
        create_project(name = name,
                       patches = patches,
                       habitat = habitat,
                       nomerge = nomerge,
                       minarea = minarea,
                       maxsize = maxsize,
                       connexity = connexity,
                       directory = directory
                       )
    
    def create_linkset(self,
                       disttype,
                       linkname,
                       threshold,
                       complete = True,
                       cost_raster = None
                       ):
        create_linkset(project = self.project_file,
                       linkname = linkname,
                       threshold = threshold,
                       complete = complete,
                       cost_raster = cost_raster
                       )
        
        if self.linksets is None:
            self.linksets = [linkname]
        
        else:
            self.linksets.append(linkname)
    
    def create_graph(self,
                     graphname,
                     linkset = None,
                     nointra = True,
                     threshold = None
                     ):
        if self.linksets is None:
            mssg = "No linksets were created yet. Use create_linkset to " + \
                "create a linkset first."
            
            raise Exception(mssg)
        
        if linkset is None:
            linkset = self.linksets[0]
        
        create_graph(graphname,
                     project = self.project_file,
                     linkset = linkset,
                     nointra = nointra,
                     threshold = threshold
                     )
        
        if self.graphs is None:
            self.graphs = [graphname]
        
        else:
            self.graphs.append(graphname)
    
    def calculate_metric(self,
                         metric,
                         linkset = None,
                         graph = None,
                         mtype = "global"):
        
        if linkset is None:
            linkset = self.linksets[0]
        
        if graph is None:
            graph = self.graphs[0]
        
        calculate_metric(project = self.project_file,
                         linkset = linkset,
                         graph = graph,
                         metric = metric,
                         mtype = mtype
                         )