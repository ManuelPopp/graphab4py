#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
import xmltodict
import xml.etree.ElementTree as ET
from urllib.request import urlretrieve
import numpy as np
import pickle as pk
import matplotlib
try:
    import matplotlib.pyplot as plt

except:
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

process_ids = []

def sigterm_handler(signum, frame):
    print("Process will be terminated. Cleaning up...")
    for pid in process_ids:
        os.kill(pid, signal.SIGTERM)
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)

_cfg_dir = os.path.join(os.path.dirname(__file__), "etc")
_cfg_file = "Settings.cfg"

if not os.path.exists(_cfg_dir):
    os.makedirs(_cfg_dir)

#-----------------------------------------------------------------------------|
# Functions
def _get_settings(file = os.path.join(_cfg_dir, _cfg_file), silent = False):
    '''
    Read Graphab4py settings from config directory.
    
    Parameters
    ----------
    file : str, optional
        Config file.
    
    silent : bool
        Return message if the config file was not found. The default is False.
    
    Returns
    -------
    ga_settings : dict
        Graphab4py settings.
    
    '''
    if os.path.isfile(file):
        with open(file, "rb") as f:
            ga_settings = pk.load(f)
    
    else:
        if not silent:
            warnings.warn(
                f"No config file found at {file}. Returning default."
                )
        
        ga_settings = {"java" : None,
                       "memory" : None,
                       "cores" : None,
                       "graphab" : None
                       }
    
    return ga_settings

def _write_settings(settings, file = os.path.join(_cfg_dir, _cfg_file)):
    try:
        with open(file, "wb") as f:
            pk.dump(settings, f)
    
    except:
        print(f"Info: Failed to save Graphab settings to {file}.")

def _delete_settings(file = os.path.join(_cfg_dir, _cfg_file)):
    '''
    Delete config file.
    
    Parameters
    ----------
    file : str, optional
        File location.
    
    Returns
    -------
    None.
    
    '''
    os.remove(file)

def try_java(java):
    '''
    Try to receive and print the Java version from the given path or shortcut.
    
    Parameters
    ----------
    java : str
        Path or shortcut to Java executable.
    
    Raises
    ------
    FileNotFoundError
        Raises error if Python fails to contact Java via subprocess and to
        return the Java version.
    
    Returns
    -------
    None.
    
    '''
    try:
        out = subprocess.run(
            [java, "-version"], stderr = subprocess.PIPE, text = True
            )
        
        version_line = out.stderr.splitlines()[0]
        version = version_line.split()[2].strip('""')
        
        print(f"Found Java version {version}.")
    
    except:
        raise FileNotFoundError(java)

def set_java(path):
    '''
    Set Java executable. This approach will set the Jaca path across sessions.
    
    Parameters
    ----------
    path : str
        Path or shortcut to Java executable.
    
    Raises
    ------
    Exception
        FileNotFoundError.
        Raises error if Python fails to contact Java via subprocess and to
        return the Java version.
    
    Returns
    -------
    None.
    
    '''
    try:
        try_java(path)
        
        global ga_settings
        ga_settings["java"] = path
        
        _ga_settings = _get_settings(silent = True)
        _ga_settings["java"] = path
        
        _write_settings(_ga_settings)
    
    except FileNotFoundError:
        raise Exception(f"Unable to locate Java at {path}.")
    
def set_graphab(path):
    '''
    Set directory to Graphab. This approach will set the Graphab path across
    sessions.
    
    Parameters
    ----------
    path : str
        Graphab .jar file or directory containing exactly one version of
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
            
            raise FileNotFoundError(mssg)
        
        path = ga_file[0]
    
    elif os.path.isfile(path):
        if os.path.splitext(path)[1] != ".jar":
            
            raise ValueError("Graphab file must be a *.jar file.")
    
    else:
        raise FileNotFoundError(f"No such file or directory: {path}.")
    
    global ga_settings
    ga_settings["graphab"] = path
    
    _ga_settings = _get_settings(silent = True)
    _ga_settings["graphab"] = path
    
    _write_settings(_ga_settings)
    
    return

def get_graphab(directory):
    '''
    Download the Graphab .jar file.
    
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
    url = "https://thema.univ-fcomte.fr/productions/" + \
        "download.php?name=graphab&version=2.8&username=Graph4lg&institution=R"
    exit_status = urlretrieve(url, filename)
    
    set_graphab(filename)
    
    return exit_status

#-----------------------------------------------------------------------------|
# Settings
ga_settings = _get_settings(silent = True)

if ga_settings["graphab"] is None:
    mssg = "No previous Graphab4py settings found. " + \
        "Use get_graphab() to download Graphab or set_graphab() to point" + \
            " Graphab4py to an existing Graphab installation."
    
    print(mssg)

sys_java = "/usr/bin/java" if platform.system() == "Linux" else "java"
java_warning = "Unable to locate Java. Please set\n" + \
"graphab4py.project.ga_settings['java'] = '/path/to/java'\n" + \
"to set the path for this session. In order to store the Java " + \
"path across sessions, use graphab4py.project.set_java(). Graphab4py may " + \
"try to locate a Java executable, but this is less secure than setting a path."

if "java" not in ga_settings.keys():
    try:
        try_java(sys_java)
        
        ga_settings = {"java" : sys_java,
                       "memory" : None,
                       "cores" : None,
                       "graphab" : None
                       }
    
    except FileNotFoundError:
        warnings.warn(
            message = java_warning,
            category = UserWarning
            )

else:
    try:
        try_java(ga_settings["java"])
    
    except FileNotFoundError:
        warnings.warn(
            message = java_warning,
            category = UserWarning
            )

#-----------------------------------------------------------------------------|
# Classes
class DistanceConverter():
    def __init__(self,
                 linkset_info,
                 regression,
                 lower_limit = None,
                 upper_limit = None
                 ):
        '''
        Create a DistanceConverter object to translate euclidean distances into
        estimated cost distances.
        
        Parameters
        ----------
        linkset_info : str
            Linkset data file containing distance values for each link.
        regression : str {"linzero", "linear", "log-log"}
            Type of the regression model. Must be "linzero" for linear
            regression through the origin, "linear" for ordinary linear
            regression, or "log-log" for regression in double-log-transformed
            space.
        lower_limit : numeric, optional
            Minimum euclidean distance to consider for the regression.
            The default is None.
        upper_limit : numeric, optional
            Maximum euclidean distance to consider for the regression.
            The default is None.
        
        Raises
        ------
        TypeError
            DESCRIPTION.
        ValueError
            DESCRIPTION.
        
        Returns
        -------
        None.

        '''
        # Check input
        if lower_limit is not None:
            try:
                lower_limit = float(lower_limit)
            
            except:
                t = type(lower_limit)
                raise TypeError(
                    f"Invalid data type {t} for 'lower_limit'. Must be numeric."
                    )
            
            if lower_limit < 0:
                raise ValueError(
                    f"Invalid value for {lower_limit}. Must be positive."
                    )
        
        if upper_limit is not None:
            try:
                upper_limit = float(upper_limit)
            
            except:
                t = type(upper_limit)
                raise TypeError(
                    f"Invalid data type {t} for 'upper_limit'. Must be numeric."
                    )
            
            if upper_limit < 0:
                raise ValueError(
                    f"Invalid value for {upper_limit}. Must be positive."
                    )
        
        self.limits = [lower_limit, upper_limit]
        
        # Open data table
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
        
        # Fit model
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
        '''
        Estimate cumulative cost for a given euclidean distance "x".
        
        Parameters
        ----------
        x : numeric
            Euclidean distance.
        
        Returns
        -------
        y : float
            Estimated cumulative cost.

        '''
        if self.regression == "linzero":
            y = self.params[0] * x
        
        elif self.regression == "linear":
            y = self.params[0] * x + self.params[1]
        
        else:
            y = np.exp(self.params[0] * np.log(x) + self.params[1])
        
        return y
    
    def show_plot(self):
        '''
        Distplay regression plot.
        
        Returns
        -------
        None.

        '''
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
        '''
        Save regression plot to file.
        
        Parameters
        ----------
        file : str
            Output file.
        
        Returns
        -------
        None.

        '''
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
        self.dist_converters = None
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
            Path to the Graphab .jar file. The default is None.
        
        :param kwargs:
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
        
        if java is None:
            try:
                global sys_java
                try_java(sys_java)
                java = sys_java
            
            except:
                raise Exception("Java path not set. Use set_java().")
        
        graphab = current_settings["graphab"].replace("\\", "/")
        
        if graphab is None:
            raise Exception("Graphab directory not set. Use set_graphab().")
        
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
            
            proc_out_b, proc_err_b = process.communicate()
            
            try:
                proc_out = proc_out_b.decode("utf-8")
            
            except AttributeError:
                proc_out = proc_out_b
            
            try:
                proc_err = proc_err_b.decode("utf-8")
            except AttributeError:
                proc_err = proc_err_b
            
            process_ids.pop()
        
        except FileNotFoundError:
            
            raise FileNotFoundError(f"Unable to locate {java}.")
        
        if "Exception" in proc_err:
            warnings.warn(proc_err)
        
        return proc_out, proc_err
    
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
                       overwrite = False,
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
        overwrite : bool, optional
            Overwrite Graphab project if a project already exists at the
            given location.
        
        :param kwargs:
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
        
        if not os.path.isdir(self.directory):
            try:
                os.makedirs(self.directory, exist_ok = False)
            
            except:
                in_dir = self.directory
                self.directory = None
                
                raise Exception(f"Cannot create directory {in_dir}.")
        
        if os.path.isfile(self.project_file):
            if overwrite:
                warnings.warn(
                    f"Project {self.project_file} already exists and will be" +
                    "replaced."
                    )
            
            else:
                warnings.warn(
                    f"Project {self.project_file} already exists. " +
                    "To overwrite it, use 'overwrite' = True."
                    )
                
                return
        
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
        
        proc_out, proc_err = self._base_call(
            **ga_settings, create = project_settings
            )
        
        out = {"process_output" : proc_out,
               "project_file" : os.path.join(directory, name, name + ".xml")
               }
        
        if "not integer" in proc_err:
            raise TypeError(
                f"Invalid data type for {patches}. " +
                "Raster values must be INT2S."
                )
        
        if not os.path.isfile(self.project_file):
            raise Exception(
                "Failed to create Graphab project. " +
                f"Graphab output: {proc_out}."
                )
        
        if "project_file" in out:
            print("Project created.")
        
        return
    
    def load_project(self, project_file, **ga_settings):
        '''
        Load an existing Graphab or Graphab4py project.
        
        Parameters
        ----------
        project_file : str
            File path of the project file (either an .xml or a .g4p file).
        
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
            
            proc_out, proc_err = self._base_call(
                **ga_settings, project = project_file, show = []
                )
            
            out_components = re.split(r"\=+", str(proc_out))
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
                "(must be either .xml or .g4p)."
                )
    
    def load_project_xml(self, project_file, **ga_settings):
        '''
        Load an existing Graphab project.
        
        Parameters
        ----------
        project_file : str
            File path of the project file (either an .xml or a .g4p file).
        
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
            
            tree = ET.parse(project_file)
            xml_data = tree.getroot()
            xml = ET.tostring(xml_data, encoding = "utf-8", method = "xml")
            data = dict(xmltodict.parse(xml))
            prj_info = data["Project"]
            self.patches = None
            self.habitat = int(prj_info["patchCodes"]["int"])
            self.nomerge = not bool(prj_info["merge"])
            self.nodata = prj_info["noData"]
            minarea = float(prj_info["minArea"])
            self.minarea = None if minarea == 0 else minarea
            maxsize = float(prj_info["maxSize"])
            self.maxsize = None if maxsize == 0 else maxsize
            self.connexity = 8 if prj_info["con8"] == "true" else 4
            self.directory = os.path.dirname(project_file)
            self.project_file = project_file
            
            if "costLinks" in prj_info.keys():
                entry = prj_info["costLinks"]["entry"]
                if isinstance(entry, list):
                    self.linksets = [ls["Linkset"]["name"] for ls in entry]
                    
                elif isinstance(entry, dict):
                    self.linksets = [entry["Linkset"]["name"]]
            
            if "graphs" in prj_info.keys():
                entry = prj_info["graphs"]["entry"]
                if isinstance(entry, list):
                    self.graphs = [g["Graph"]["name"] for g in entry]
                
                elif isinstance(entry, dict):
                    self.graphs = [entry["Graph"]["name"]]
            
            if "pointsets" in prj_info.keys():
                entry = prj_info["pointsets"]["entry"]
                if isinstance(entry, list):
                    self.pointsets = [p["Pointset"]["name"] for p in entry]
                
                elif isinstance(entry, dict):
                    self.pointsets = [entry["Pointset"]["name"]]
    
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
            Path to an external cost raster file (.tif). The default is None.
        
        :param kwargs:
            Additional Graphab settings.
        
        Returns
        -------
        proc_out : bytes
            Process output.

        '''
        disttype = disttype.lower()
        
        if disttype not in ["euclid", "cost"]:
            raise ValueError(
                f"Invalid value {disttype} to argument disttype." +
                "Must be either 'euclid' or 'cost'."
                )
        
        if disttype == "cost":
            if isinstance(cost_raster, str):
                if not os.path.isfile(cost_raster):
                    raise FileNotFoundError(cost_raster)
            
            else:
                t = type(cost_raster)
                raise TypeError(
                    f"Invalid data type {t} for argument cost_raster." +
                    " Must be of type 'str'. Note that for disttype == " +
                    "'cost', a resistance surface must be provided as a " +
                    "raster file."
                    )
        
        link_settings = [f"distance={disttype}", f"name={linkname}"]
        
        if complete:
            link_settings += ["complete"]
        
        if threshold:
            try:
                float(threshold)
                link_settings += [f"maxcost={threshold}"]
            
            except:
                raise TypeError(
                    f"Invalid data type {t} provided to argument " +
                    "'threshold'. Must be numeric."
                    )
        
        if cost_raster is not None:
            link_settings += [f"extcost={cost_raster}"]
        
        proc_out, proc_err = self._base_call(
            **ga_settings, project = self.project_file, linkset = link_settings
            )
        
        if self.linksets is None:
            self.linksets = [linkname]
        
        else:
            self.linksets.append(linkname)
        
        if "canceled" in proc_out:
            raise Exception(
                "Failed to create linkset. Check resistance surface." +
                "Check input parameters and ressource usage."
                )
        
        elif "100.0%" in proc_out:
            print("Linkset created.")
        
        return
    
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
        
        :param kwargs:
            Additional Graphab settings.
        
        Returns
        -------
        proc_out : bytes
            Process output.

        '''
        if self.linksets is None:
            raise Exception(
                "No linksets were created yet. Use create_linkset to " +
                "create a linkset first."
                )
        
        elif linkset is None:
            linkset = self.linksets[0]
        
        elif linkset not in self.linksets:
            raise ValueError(
                f"Linkset '{linkset}' not found. Use create_linkset to " +
                "create a new linkset or call attribute .linksets to list " +
                "existing linksets."
                )
        
        graph_settings = [f"name={graphname}"]
        
        if nointra:
            graph_settings += ["nointra"]
        
        if threshold is not None:
            try:
                float(threshold)
                graph_settings += [f"threshold={threshold}"]
            
            except:
                t = type(threshold)
                raise TypeError(
                    f"Invalid data type {t} provided to argument 'threshold'."
                    )
        
        proc_out, proc_err = self._base_call(
            **ga_settings, project = self.project_file, uselinkset = linkset,
            graph = graph_settings
            )
        
        if self.graphs is None:
            self.graphs = [graphname]
        
        else:
            self.graphs.append(graphname)
        
        if "Exception" in proc_out:
            warnings.warn(proc_err)
        
        elif "100%" in proc_out:
            print("Graph created.")
        
        return
    
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
        
        :param kwargs:
            Metric paramneters; 
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
        
        #Python >= 10
        #match mtype:
        #    case "global":
        #        metric = {"gmetric" : metric_settings}
        #    
        #    case "component":
        #        metric = {"cmetric" : metric_settings}
        #    
        #    case "local":
        #        metric = {"lmetric" : metric_settings}
        #    
        #    case _:
        #        raise Exception(f"Illegal argument for mtype: {mtype}.")
        
        # BEGIN ALTERNATIVE FOR OLD PYTHON VERSIONS
        if mtype == "global":
            metric = {"gmetric" : metric_settings}
        
        elif mtype == "component":
            metric = {"cmetric" : metric_settings}
        
        elif mtype == "local":
            metric = {"lmetric" : metric_settings}
        
        else:
            raise Exception(f"Illegal argument for mtype: {mtype}.")
        # END
        
        proc_out, proc_err = self._base_call(
            **ga_settings, project = self.project_file, uselinkset = linkset,
            usegraph = graph, **metric
            )
        
        try:
            metric_value = float(
                proc_out.split(" ")[-1].strip().strip("}").strip("]")
                )
            
            out = {"process_output" : proc_out,
                   "metric_value" : metric_value}
        
        except:
            if "Exception" in proc_out:
                out = proc_err
                
                if "Access is denied" in proc_out:
                    raise Exception(
                        "Directory not writeable. Access is denied."
                        )
            
            else:
                out = proc_out
        
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
            Restrict the calculations on items listed in a .txt file. The file
            must contain one identifier per line. The default is None.
        obj : str {patch, link}, optional
            Type of objects to remove. The default is "patch".
        mpi : bool, optional
            Run in MPI mode (on cluster).
        
        :param kwargs:
            Metric paramneters;
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
        
        proc_out, proc_err = self._base_call(
            **ga_settings, project = self.project_file, uselinkset = linkset,
            usegraph = graph, mpi = mpi, delta = delta_settings
            )
        
        return
    
    def enable_distance_conversion(self,
                            linkset = None,
                            regression = "linzero",
                            show_plot = False,
                            save_plot = False,
                            min_euc = None,
                            max_euc = None,
                            **kwargs# Make sure a dict can be passed w/out error
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
        min_euc : float, optional
            Minimum euclidean distance to consider for the regression.
        max_euc : float, optional
            Maximum euclidean distance to consider for the regression.
        
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
        
        if not isinstance(self.dist_converters, dict):
            self.dist_converters = dict()
            self.dist_converters[linkset] = dict()
        
        elif not isinstance(self.dist_converters[linkset], dict):
            self.dist_converters[linkset] = dict()
        
        self.dist_converters[linkset][regression] = DistanceConverter(
            linkset_info, regression,
            lower_limit = min_euc, upper_limit = max_euc
            )
        
        if show_plot:
            self.dist_converters[linkset][regression].show_plot()
        
        if save_plot:
            self.dist_converters[linkset][regression].save_plot(save_plot)
        
    def convert_distance(self,
                         x,
                         linkset = None,
                         regression = "linzero",
                         show_plot = False,
                         save_plot = False,
                         min_euc = None,
                         max_euc = None):
        '''
        Estimate the cumulative cost along an euclidean distance. If no
        euclid-to-cost relationship has been established yet, the method first
        calls enable_distance_conversion().
        
        Parameters
        ----------
        x : numeric
            Euclidean distance for which cumulative cost is to be estimated.
        linkset : str, optional
            Name of the linkset to use. The default is None.
        regression : str in {log, linear, linearzero}, optional
            Regression type. One in log (log-log regression), linear (simple
            linear regression), or linorig (linear regression forced through
            the origin). The default is "linearzero".
        min_euc : float, optional
            Minimum euclidean distance to consider for the regression.
        max_euc : float, optional
            Maximum euclidean distance to consider for the regression.
        
        Returns
        -------
        cost : float
            Estimated cumulative cost corresponding to an euclidean distance
            of "x".

        '''
        try:
            x = float(x)
        
        except:
            t = type(x)
            raise TypeError(f"Invalid data type {t} for argument 'x'.")
        
        if x < 0.:
            raise ValueError(
                "Distance 'x' must be positive. Negative value {x} provided."
                )
        
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
        
        try:
            try:
                limits = self.dist_converters[linkset][regression].limits
            
            except:
                raise Warning(
                    "No euclid-to-cost relationship established yet. " +
                    "Regression will be started. This might take a moment."
                    )
            
            if min_euc is not None:
                if min_euc != limits[0]:
                    raise Warning(
                    f"New lower limit {min_euc} set. New regression model is" +
                    " being fit."
                    )
            
            if max_euc is not None:
                if max_euc != limits[1]:
                    raise Warning(
                    f"New upper limit {max_euc} set. New regression model is" +
                    " being fit."
                    )
            
            cost = self.dist_converters[linkset][regression].predict_cost(x)
        
        except Warning as w:
            warnings.warn(w)
            arguments = locals()
            x = arguments.pop("x")
            _ = arguments.pop("self")
            _ = arguments.pop("w")
            self.enable_distance_conversion(**arguments)
            
            cost = self.dist_converters[linkset][regression].predict_cost(x)
        
        return cost
