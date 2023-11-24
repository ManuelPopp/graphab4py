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
import os, sys, re, glob, platform, subprocess, signal, warnings, csv
from urllib.request import urlretrieve
import numpy as np
import pickle as pk
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

java = "/usr/bin/java" if platform.system() == "Linux" else "java"
_init_dir = os.path.dirname(__file__)

try:
    with(open(os.path.join(_init_dir, "Settings.pkl")), "rb") as f:
        ga_settings = pk.read(f)

except:
    mssg = "No previous Graphab4py settings found. " + \
        "Use get_graphab() to download Graphab or set_graphab() to point" + \
            " Graphab4py to an existing Graphab installation."
    print(mssg)

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
        
        path = ga_file[0]
    
    elif os.path.isfile(path):
        if os.path.splitext(path)[1] != ".jar":
            
            raise Exception("Graphab file must be a *.jar file.")
    
    else:
        raise Exception(f"No such file or directory: {path}.")
    
    global ga_settings
    ga_settings["graphab"] = path
    
    settings_file = os.path.join(_init_dir, "Settings.pkl")
    
    try:
        with open(settings_file, "wb") as f:
            pk.dump(ga_settings, f)
    
    except:
        print("Info: Failed to save Graphab settings to {settings_file}.")
    
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
    
    print("Downloading Graphab...")
    url = "https://thema.univ-fcomte.fr/productions/download.php?name=graphab&version=2.8&username=Graph4lg&institution=R"
    exit_status = urlretrieve(url, filename)
    
    set_graphab(filename)
    
    return exit_status

#-----------------------------------------------------------------------------|
# Classes
class DistanceConverter():
    def __init__(self,
                 linkset_info,
                 regression,
                 lower_limit = None,
                 upper_limit = None
                 ):
        with open(linkset_info, newline = "\n") as f:
            reader = csv.reader(f, delimiter = ",", quotechar = '"')
            
            dist_l = []
            distM_l = []
            for row in reader:
                _, _, d, dM = row
                dist_l.append(d)
                distM_l.append(dM)
            
            dist = np.array(dist_l[1:]).astype("float")
            distM = np.array(distM_l[1:]).astype("float")
            
            if (lower_limit is not None) and (upper_limit is not None):
                indices = np.where(distM >= lower_limit & distM <= upper_limit)
            
            elif lower_limit is not None:
                indices = np.where(distM >= lower_limit)
            
            elif upper_limit is not None:
                indices = np.where(distM <= upper_limit)
            
            else:
                indices = range(len(distM))
            
            self.dist = dist[indices]
            self.distM = distM[indices]
        
        if regression.lower() == "linzero":
            self.regression = "linzero"
            self.x, self.y = self.distM, self.dist
            self.x = self.x[:, np.newaxis]
            
            m, residuals, rank, s = np.linalg.lstsq(self.x, self.y)
            self.params = [m, 0]
        
        elif regression.lower() == "linear":
            self.regression = "linear"
            self.x, self.y = self.distM, self.dist
            
            [m, b], rss, rank, _, _ = np.polyfit(
                self.x, self.y, 1, full = True
                )
            
            self.params = [m, b]
            
        elif regression.lower() in ["log", "log-log", "loglog"]:
            self.regression = "log"
            self.x = np.log(self.distM)
            self.y = np.log(self.dist)
            
            [m, b], rss, rank, _, _ = np.polyfit(
                self.x, self.y, 1, full = True
                )
            
            self.params = [m, b]
        
        else:
            raise ValueError(f"Invalid value '{regression}'.")
    
    def predict_cost(self, x):
        if self.regression == "linzero":
            y = self.params[0] * x
        
        elif self.regression == "linear":
            y = self.params[0] * x + self.params[1]
        
        else:
            y = np.exp(self.params[0] * np.log(x) + self.params[1])
        
        return y
    
    def show_plot(self):
        if self.regression == "log":
            xlab = "log distance"
            ylab = "log cumulative cost"
        
        else:
            xlab = "Distance (m)"
            ylab = "Cumulative cost"
        
        plt.xlabel(xlab)
        plt.ylabel(ylab)
        plt.plot(self.x, self.y, "o")
        plt.plot(self.x, self.params[0] * self.x + self.params[1])
        plt.show()
    
    def save_plot(self, file):
        if self.regression == "log":
            xlab = "log DistM"
            ylab = "log Dist"
        else:
            xlab = "DistM"
            ylab = "Dist"
        
        plt.xlabel(xlab)
        plt.ylabel(ylab)
        plt.plot(self.x, self.y, "o")
        plt.plot(self.x, self.params[0] * self.x + self.params[1])
        plt.savefig(file)

class Project():
    def __init__(self):
        pass
    
    def _base_call(self, java = None, memory = None, cores = None,
                  graphab = None, **kwargs):
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
        
        settings = {
            key : val for key, val in locals().items() if (
                (val is not None) and (
                    key in ["java", "memory", "cores", "graphab"]
                    )
                )
            }
        
        if len(settings) > 0:
            current_settings.update(settings)
        
        java = current_settings["java"]
        graphab = current_settings["graphab"].replace("\\", "/")
        
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
        print(cmd)
        
        try:
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
        
        except FileNotFoundError:
            proc_out = 1
            
            raise FileNotFoundError(f"Cannot find {java}.")
        
        return proc_out
    
    def create_project(self,
                       name,
                       patches,
                       habitat,
                       nomerge = False,
                       nodata = None,
                       minarea = None,
                       maxsize = None,
                       connexity = 8,
                       directory = None,
                       **ga_settings
                       ):
        '''
        Create a Graphab project.
        
        Parameters
        ----------
        name : str
            Project name.
        patches : str
            File path of the patches file. Patches must be a raster containing
            values encoded as INT2S.
        habitat : int
            Integer(s) indicating habitat patches.
        nomerge : bool, optional
            DESCRIPTION. The default is False.
        nodata : int, optional
            NoData value. The default is None.
        minarea : TYPE, optional
            DESCRIPTION. The default is None.
        maxsize : TYPE, optional
            DESCRIPTION. The default is None.
        connexity : int in {4, 8}, optional
            Consider the 4 or 8 neighbours when merging pixels to patches.
            The default is 8.
        directory : str, optional
            Directory in which the project shall be created. If set to none,
            the current working directory is used. The default is None.
        **ga_settings : dict
            Dictionary containing Graphab settings.
        
        Returns
        -------
        out : dict
            A dictionary containing process output and project name.
        '''
        self.name = name
        self.patches = patches
        self.habitat = habitat
        self.nomerge = nomerge
        self.nodata = nodata
        self.minarea = minarea
        self.maxsize = maxsize
        self.connexity = connexity
        self.directory = os.getcwd() if directory is None else directory \
            .replace("\\", "/")
        self.project_file = os.path.join(directory, name, name + ".xml")
        self.linksets = None
        self.graphs = None
        self.pointsets = None
        
        project_settings = [name,
                            patches,
                            f"habitat={habitat}"
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
        
        project_settings += [f"dir={directory}"]
        
        proc_out = self._base_call(**ga_settings, create = project_settings)
        
        out = {"process_output" : proc_out,
               "project_file" : os.path.join(directory, name, name + ".xml")
               }
        
        if not os.path.isfile(self.project_file):
            mssg = "Failed to create Graphab project. Graphab output: {}"
            
            raise Exception(mssg.format(proc_out))
        
        return out
    
    def load_project(self, project_file, **ga_settings):
        '''
        Load an existing Graphab or Graphab4py project.
        
        Parameters
        ----------
        project_file : str
            File path of the project file (either an *.xml or a *.g4p file).
        
        Returns
        -------
        None.
        '''
        if os.path.isfile(project_file):
            dir_f = project_file
        
        elif os.path.isfile(os.path.join(os.getcwd(), project_file)):
            dir_f = os.path.join(os.getcwd(), project_file)
        
        else:
            raise FileNotFoundError(f"File not found: {project_file}.")
        
        if os.path.splitext(dir_f)[1] == ".g4p":
            with open(dir_f, "rb") as f:
                proj = pk.load(f)
            
            self.__dict__.update(proj.__dict__)
        
        elif os.path.splitext(dir_f)[1] == ".xml":
            self.name = os.path.basename(os.path.splitext(dir_f)[0])
            
            out = self._base_call(
                **ga_settings, project = project_file, show = []
                )
            
            out_components = re.split(r"\=+", str(out))
            output = [
                o.replace("\\n", "").replace("\\r", "").strip(" ")
                for o in out_components
                ]
            linksets_start = output.index("Link sets") + 1
            graphs_start = output.index("Graphs") + 1
            pointsets_start = output.index("Point sets") + 1
            
            if output.index("Graphs") > linksets_start:
                linksets = output[linksets_start : output.index("Graphs")]
                linksets = [l for l in linksets if l not in ["", "'"]]
            
            if output.index("Point sets") > graphs_start:
                graphs = output[graphs_start : output.index("Point sets")]
                graphs = [g for g in graphs if g not in ["", "'"]]
            
            pointsets = output[pointsets_start:]
            pointsets = [p for p in pointsets if p not in ["", "'"]]
            
            self.linksets = None if linksets == [] else linksets
            self.graphs = None if graphs == [] else graphs
            self.pointsets = None if pointsets == [] else pointsets
        
        else:
            raise ValueError(
                "Project file path does not end with a valid extension" +
                "(must be either *.xml or *.g4p)."
                )
    
    def save(self):
        '''
        Save current instance.
        
        Returns
        -------
        None.
        '''
        try:
            file = os.path.join(self.directory, self.name + ".g4p")
        
        except:
            raise Exception(
                "Failed to create project path." +
                " Have you created a project already?"
                )
        
        with open(file, "wb") as f:
            pk.dump(self, f)
        
        print(f"Output saved at {file}.")
    
    def create_linkset(self, disttype, linkname, threshold, complete = True,
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
            Maximum distance or maximum accumulated cost (depending on the type
            of distance).
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
        
        proc_out = self._base_call(**ga_settings, project = self.project_file,
                             linkset = link_settings)
        
        if self.linksets is None:
            self.linksets = [linkname]
        
        else:
            self.linksets.append(linkname)
        
        return proc_out
    
    def create_graph(self, graphname, linkset = None, nointra = True,
                     threshold = None, **ga_settings):
        '''
        Create a graph.
        
        Parameters
        ----------
        graphname : str
            Graph name.
        linkset : str
            Name of the linkset. The default is None.
        nointra : bool, optional
            Set the "nointra" option. The default is True.
        threshold : int, optional
            Maximum distance or maximum accumulated cost (depending on the type
            of distance). The default is None.
        **ga_settings : any
            Additional Graphab settings.
        
        Returns
        -------
        proc_out : bytes
            Process output.
        '''
        if self.linksets is None:
            mssg = "No linksets were created yet. Use create_linkset to " + \
                "create a linkset first."
            
            raise Exception(mssg)
        
        elif linkset is None:
            linkset = self.linksets[0]
        
        elif linkset not in self.linksets:
            mssg = f"Linkset '{linkset}' not found. Use create_linkset to " + \
                "create a new linkset or call attribute .linksets to list " + \
                    "existing linksets."
            
            raise ValueError(mssg)
        
        graph_settings = [f"name={graphname}"]
        
        if nointra:
            graph_settings += ["nointra"]
        
        if threshold is not None:
            graph_settings += [f"threshold={threshold}"]
        
        proc_out = self._base_call(**ga_settings, project = self.project_file,
                             uselinkset = linkset, graph = graph_settings)
        
        if self.graphs is None:
            self.graphs = [graphname]
        
        else:
            self.graphs.append(graphname)
        
        return proc_out
    
    def calculate_metric(self, metric, linkset = None, graph = None,
                         mtype = "global", **metric_args):
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
        if self.linksets is None:
            mssg = "No linksets were created yet. Use create_linkset to " + \
                "create a linkset first."
            
            raise Exception(mssg)
        
        elif linkset is None:
            linkset = self.linksets[0]
        
        elif linkset not in self.linksets:
            mssg = f"Linkset '{linkset}' not found. Use create_linkset to " + \
                "create a new linkset or call attribute .linksets to list " + \
                    "existing linksets."
            
            raise ValueError(mssg)
        
        if self.graphs is None:
            mssg = "No graph were created yet. Use create_graph to " + \
                "create a graph first."
            
            raise Exception(mssg)
        
        elif graph is None:
            graph = self.graphs[0]
        
        elif graph not in self.graphs:
            mssg = f"Graph '{graph}' not found. Use create_graph to " + \
                "create a new graph or call attribute .graphs to list " + \
                    "existing graphs."
            
            raise ValueError(mssg)
        
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
        
        proc_out = self._base_call(**ga_settings, project = self.project_file,
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
    
    def delta_by_item(self, metric, linkset = None, graph = None,
                    select = None, select_from_file = None, obj = "patch",
                    mpi = False, **metric_args):
        '''
        Calculate a global metric in delta mode on patches or links depending
        on obj parameter for the selected graph.
        
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
        if self.linksets is None:
            mssg = "No linksets were created yet. Use create_linkset to " + \
                "create a linkset first."
            
            raise Exception(mssg)
        
        elif linkset is None:
            linkset = self.linksets[0]
        
        elif linkset not in self.linksets:
            mssg = f"Linkset '{linkset}' not found. Use create_linkset to " + \
                "create a new linkset or call attribute .linksets to list " + \
                    "existing linksets."
            
            raise ValueError(mssg)
        
        if self.graphs is None:
            mssg = "No graph were created yet. Use create_graph to " + \
                "create a graph first."
            
            raise Exception(mssg)
        
        elif graph is None:
            graph = self.graphs[0]
        
        elif graph not in self.graphs:
            mssg = f"Graph '{graph}' not found. Use create_graph to " + \
                "create a new graph or call attribute .graphs to list " + \
                    "existing graphs."
            
            raise ValueError(mssg)
        
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
        
        proc_out = self._base_call(**ga_settings, project = self.project_file,
                             uselinkset = linkset, usegraph = graph, mpi = mpi,
                             delta = delta_settings)
        
        return
    
    def distance_conversion(self,
                            linkset = None,
                            regression = "linorig",
                            show_plot = False,
                            save_plot = False
                            ):
        '''
        Establish a relationship between euclidean and cost distance.
        
        Parameters
        ----------
        linkset : str, optional
            Name of the linkset to use. The default is None.
        regression : str in {log, linear, linearzero}, optional
            Regression type. One in log (log-log regression), linear (simple
            linear regression), or linorig (linear regression forced through
            the origin). The default is "linearzero".
        
        Returns
        -------
        None.
        '''
        if self.linksets is None:
            mssg = "No linksets were created yet. Use create_linkset to " + \
                "create a linkset first."
            
            raise Exception(mssg)
        
        elif linkset is None:
            linkset = self.linksets[0]
        
        elif linkset not in self.linksets:
            mssg = f"Linkset '{linkset}' not found. Use create_linkset to " + \
                "create a new linkset or call attribute .linksets to list " + \
                    "existing linksets."
            
            raise ValueError(mssg)
        
        linkset_info = os.path.join(
            os.path.dirname(self.project_file),
            linkset + "-links.csv"
            )
        
        self.DistConv = DistanceConverter(linkset_info, regression)
        
        if show_plot:
            self.DistConv.show_plot()
        
        if save_plot:
            self.DistConv.show_plot(save_plot)