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

    Attributes:
        workspaces (dict(str,Workspace)): All the workspaces
        current_workspace (str): The current workspace
    """
    def __init__(self):
        """Initialize a workspace manager.
        """
        self.workspaces = dict()
        self.current_workspace = ""

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
            path (str): The absolute path of the workspace. Default is "".
        """
        ws = Workspace(name,path)
        self.workspaces[path] = ws
        self.current_workspace = path
        print(ws)

    def delete_workspace(self, workspace_path):
        """ Delete the workspace identified by its abolute path.

        Args:
            workspace_path (str): The absolute path of the workspace to delete.

        Raises:
            AssertionError: If the workspace directory does not exist or can not be deleted.
        """
        assert (workspace_path in self.workspaces),\
                "The workspace "+ workspace_path +" does not exist in the workspace manager."
        self.workspaces[workspace_path].delete()
        del self.workspaces[workspace_path]
        if (self.current_workspace == workspace_path):
            self.current_workspace = ""

    def get_current_workspace(self):
        """ Get the current workspace.

        Returns:
            Workspace: The current workspace.

        Raises:
            AssertionError: If no current workspace.
            AssertionError: If the current workspace has disappeared.
        """
        assert (self.current_workspace), "There is no current workspace."
        assert (self.current_workspace in self.workspaces), "The current workspace is not reachable."
        return self.workspaces[self.current_workspace]

    def set_current_workspace(self, workspace_path):
        """ Set the current workspace.

        Args:
            workspace_path (str): The absolute path of the workspace
                    which will be the current workspace.

        Raises:
            AssertionError: If the workspace does not exist in the workspace manager.
        """
        assert (workspace_path in self.workspaces), "The workspace " +\
                workspace_path + "does not exist in this workspace manager."
        self.current_workspace = workspace_path

    def new_scene(self, name="", path=""):
        """ Create a new scene in the current workspace.

        Args:
            name (str): The name of the scene.
            path (str): The local path of the scene in the workspace.

        Raises:
            AssertionError: If there is no current workspace or the scene already exists.
        """
        ws = self.get_current_workspace()
        ws.new_scene(name,path)

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
        self.path = Utils.valid_name(path)
        if not self.path:
            self.path = Utils.valid_name(self.name)
        self.scenes = dict()
        self.current_scene = ""
        self.qt_directory = QDir(self.path)
        assert (not self.qt_directory.exists()),\
                "The directory " + self.qt_directory.absolutePath() + " already exists. " + \
                "Please give a non-existing directory (it will be created)"
        assert (self.qt_directory.mkpath(".")), "The directory " +\
                self.qt_directory.absolutePath() + " can not be created."
        self.subdirs = dict()
        self.subdirs["Configs"] = "Configuration folder"
        for subpath in self.subdirs:
            self.qt_directory.mkpath(subpath)

    def delete(self):
        """ Delete the workspace (and its contents).

        It must not be called by itself but by the workspace manager !

        Raises:
            AssertionError: If the workspace directory does not exist or can not be deleted.
        """
        # Deleting the scenes
        self.current_scene = ""
        for scene_path in self.scenes:
            self.delete_scene(scene_path)
        # Deleting the workspace directory
        assert (self.qt_directory.exists()),\
                "The directory " + self.qt_directory.absolutePath() + " does not exists."
        assert (self.qt_directory.removeRecursively()),\
                "The directory " + self.qt_directory.absolutePath() + " can not be deleted."


    def new_scene(self, name="", path=""):
        """ Add a new scene to the workspace.

        Args:
            name (str): The name of the new scene
            path (str): The local path of the scene (inside workspace)

        Raises:
            AssertionError: If a scene with the same path already exists.
        """
        assert (path not in self.scenes), "A scene with that path already exists."
        scene = Scene(self, name, path)
        self.scenes[scene.path] = scene
        self.set_current_scene(scene.path)

    def delete_scene(self, scene_path):
        """ Delete the scene identified by its local path.

        Args:
            scene_path (str): The path (relatively to the workspace) of the scene to delete.
        """
        assert (scene_path in self.scenes),\
                "The scene "+ scene_path +" does not exist in the workspace."
        self.scenes[scene_path].delete()
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
        self.path = Utils.valid_name(path)
        if not self.path:
            self.path = Utils.valid_name(self.name)

    def delete(self):
        """ Delete the scene and remove its access from the workspace.

        It must not be called by itself but by the workspace !
        """
        pass

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
