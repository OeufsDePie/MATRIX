import os
import unicodedata
import string
import re                 # regular expressions
########## PyQt5 imports
from PyQt5.QtCore import QDir

class WorkspaceManager(object):
    """ Manages the workspace.

    Will handle all interactions between user and modules and the working space.
    This class is responsible for managing files inside the workspace and for
    communicating any change through signals.
    """

    def setProjectPath(self, projectPath):
        '''
        Define the root path of the project

        projectPath -- The path
        '''
        self.projectPath = projectPath

    def pictureModelPath(self):
        '''
        Retrieve the model file that sums up every piece of information about 
        pictures on the project.
        '''
        return os.path.join(self.projectPath, "pictures.xml")

    def new_workspace(self, name="", path=""):
        """ Create a new workspace.

        Args:
            name (str): The name of the workspace.
            path (str): The path of the workspace. Default is "".
        """
        ws = Workspace(name,path)
        print(ws)


class Workspace:
    """ A workspace containing its own configuration and scenes.

    Attributes:
        name (str): The name of the workspace.
        path (str): The path of the workspace.
        subdirs (dict(str,str)): The useful subdirectories (path,name)
        scenes (dict(str,Scene)): The dictionnary of the scenes it contains.
            Keys are the scene paths.
        current_scene (str): The path of the current scene
        qt_directory (QDir): The directory corresponding to that workspace
    """

    def __init__(self, name="", path=""):
        """Initialize a workspace.

        Args:
            name (str): The name of the workspace. Default is "".
            path (str): The path of the workspace. Default is "".

        Raises:
            AssertionError: If a directory with that path already exists.

        Examples:
            >>> ws = Workspace("ws1","/home/mpizenbe/matrix/ws1")
        """
        self.name = name
        self.path = path
        if not self.path:
            self.path = Utils.valid_name(self.name)
        self.scenes = dict()
        self.current_scene = ""
        self.qt_directory = QDir(self.path)
        assert (not self.qt_directory.exists()),\
                "The directory " + self.qt_directory.absolutePath() + " already exists. " + \
                "Please give a non-existing directory (it will be created)"
        self.qt_directory.mkpath(".")
        self.subdirs = dict()
        self.subdirs["Configs"] = "Configuration folder"
        for subpath in self.subdirs:
            self.qt_directory.mkpath(subpath)

    def new_scene(self, scene):
        """ Add a new scene to the workspace.

        Args:
            scene (Scene): The new scene

        Raises:
            AssertionError: If a scene with the same path already exists.
        """
        assert (scene.path not in self.scenes), "A scene with that path already exists."
        self.scenes[scene.path] = scene
        self.set_current_scene(scene.path)

    def delete_scene(self, scene_path):
        """ Delete the scene identified by its local path.

        Args:
            scene_path (str): The path (relatively to the workspace) of the scene to delete.
        """
        del self.scenes[scene_path]
        if (self.current_scene == scene_path):
            self.current_scene = ""

    def get_current_scene(self):
        """ Get the current scene of the workspace.

        Returns:
            Scene: The current scene.

        Raises:
            AssertionError: If no current scene.
            AssertionError: If the current scene has disappeared.
        """
        assert (self.current_scene), "There is no current scene."
        assert (self.current_scene in self.scenes), "The current scene is not reachable."
        return self.scenes[self.current_scene]

    def set_current_scene(self, scene_path):
        """ Set the current scene.

        Args:
            scene_path (str): The path of the scene which will be the current scene.

        Raises:
            AssertionError: If the scene does not exist in the workspace.
        """
        assert (scene_path in self.scenes), "That scene does not exist in this workspace."
        self.current_scene = scene_path

    def __str__(self):
        """ Change displaying of a workspace.

        Example:
            >>> print(workspace)
        """
        s = ["Workspace : " + self.name                     ,\
             "   path          : " + self.path              ,\
             "   current scene : " + self.current_scene     ,\
             "   all scenes    : " + str(list(self.scenes.keys()))]
        return "\n".join(s)


class Scene:
    """ A scene containing all its images.

    Attributes:
        workspace (Workspace): The workspace containing the scene.
        name (str): The name of the scene. It must be unique in the workspace.
            For example : "Shooting ENSEEIHT".
            Default is "scene_n" where n is the current number of scenes in workspace.
        path (str): The path relatively to the workspace path.
            Default is self.name
    """

    def __init__(self, workspace, name="", path=""):
        """ Initialize a scene in a workspace.

        Args:
            workspace (Workspace): The parent workspace.
            name (str): The name of the scene
            path (str): The path relatively to the current workspace

        Examples:
            >>> sc = Scene(ws)
            >>> sc = Scene(ws, "Shooting ENSEEIHT")
            >>> sc = Scene(ws, "Shooting ENSEEIHT", "shoot_n7")
        """
        self.workspace = workspace
        self.name = name
        if not name:
            self.name = "scene_" + str(len(workspace.scenes))
        self.path = path
        if not path:
            self.path = Utils.valid_name(self.name)
        workspace.new_scene(self)

    def delete(self):
        """ Delete the scene and remove its access from the workspace.
        """
        self.workspace.delete_scene(self.path)

    def __str__(self):
        """ Change displaying of a scene.

        Example:
            >>> print(scene)
        """
        s = ["Scene : " + self.name                       ,\
             "   workspace : " + self.workspace.name      ,\
             "   path      : " + self.path]
        return "\n".join(s)

class Utils:
    """ Useful functions.
    """

    def valid_name(s):
        """ Transform a string in order to get a valid filename

        This method may produce invalid filenames such as "."
        """
        # the authorized characters
        valid_chars = "-_.()/ %s%s" % (string.ascii_letters, string.digits)
        # tranform to authorized characters
        valid_string = ''.join(c for c in unicodedata.normalize('NFKD',s) if c in valid_chars)
        # remove spaces at the extremities
        valid_string = valid_string.strip()
        # replace spaces by underscores
        valid_string  = valid_string.replace(" ","_")
        # remove multiple spaces and others
        valid_string = re.sub('\.+','\.',valid_string)
        valid_string = re.sub('-+','-',valid_string)
        valid_string = re.sub('_+','_',valid_string)
        return valid_string
