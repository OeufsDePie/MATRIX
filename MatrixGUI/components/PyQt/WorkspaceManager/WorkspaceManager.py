import os
import unicodedata
import string
import re                 # regular expressions

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


class Workspace:
    """ A workspace containing its own configuration and scenes.

    Attributes:
        name (str): The name of the workspace.
        path (str): The path of the workspace.
        scenes (list(Scene)): The list of the scene names it contains.
    """

    def __init__(self, name="", path=""):
        """Initialize a workspace.

        Args:
            name (str): The name of the workspace. Default is "".
            path (str): The path of the workspace. Default is "".

        Examples:
            >>> ws = Workspace("ws1","/home/mpizenbe/matrix/ws1")
        """
        self.name = name
        self.path = path
        self.scenes = []

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
        self.path = path

class Utils:
    """ Useful functions.
    """

    def valid_name(s):
        """ Transform a string in order to get a valid filename

        This method may produce invalid filenames such as "."
        """
        # the authorized characters
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
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
