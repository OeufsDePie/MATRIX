import os, random, math
import xml.etree.cElementTree as ET
from Workspace import Workspace

class WorkspaceManager():
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

    def generateModel(self, picturesFiles):
        root = ET.Element("pictures")
        for url in picturesFiles:
            status = str(int(math.floor(4*random.random())))
            ET.SubElement(root, "picture", status=status).text = url.path()
        tree = ET.ElementTree(root)
        tree.write(self.pictureModelPath())

    def new_workspace(self, name="", base_path=""):
        """ Create a new workspace.

        Args:
            name (str): The name of the workspace.
            base_path (str): The absolute path of the directory that will contain the new workspace.
        """
        ws = Workspace(name,base_path)
        ws.create_directory()
        self.workspaces[ws.full_path()] = ws
        self.current_workspace = ws.full_path()
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
            path (str): The relative path of the scene in the workspace.

        Raises:
            AssertionError: If there is no current workspace or the scene already exists.
        """
        ws = self.get_current_workspace()
        ws.new_scene(name,path)

    def delete_scene(self, scene_path):
        """ Delete the scene identified by its path in the current workspace.

        Args:
            scene_path (str): The relative path of the scene to delete in the current workspace.

        Raises:
            AssertionError: If the scene directory does not exist or can not be deleted.
        """
        ws = self.get_current_workspace()
        assert (scene_path in ws.scenes),\
                "The scene "+ scene_path +" does not exist in the current workspace."
        ws.delete_scene(scene_path)

    def set_current_scene(self, scene_path):
        """ Change the current scene identified by its path in the current workspace.

        Args:
            scene_path (str): The relative path of the scene to select in the current workspace.

        Raises:
            AssertionError: If the scene directory does not exist or can not be deleted.
        """
        ws = self.get_current_workspace()
        assert (scene_path in ws.scenes),\
                "The scene "+ scene_path +" does not exist in the current workspace."
        ws.set_current_scene(scene_path)
