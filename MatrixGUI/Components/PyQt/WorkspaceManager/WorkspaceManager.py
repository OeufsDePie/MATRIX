import os, random, math, exiftool
import xml.etree.cElementTree as ET
from Workspace import Workspace
from PyQt5.QtCore import QStringListModel

class WorkspaceManager():
    """ Manages the workspace.

    Will handle all interactions between user and modules and the working space.
    This class is responsible for managing files inside the workspace and for
    communicating any change through signals.

    Attributes:
        workspaces (dict(str,Workspace)): All the workspaces.
        current_workspace (str): The current workspace.
        workspaces_model (QStringListModel): The list model (for qml) of the workspaces.
    """
    def __init__(self):
        """Initialize a workspace manager.
        """
        self.workspaces = dict()
        self.current_workspace = "" 
        self.workspaces_model = QStringListModel()

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
        with exiftool.ExifTool() as exifparser:
            for url in picturesFiles:
                elem = ET.SubElement(root, "picture", status="0")
                elem.text = url.path()

                # Get EXIF data
                exifData = exifparser.get_tags(\
                    ['EXIF:GPSLatitude', 'EXIF:GPSLongitude'], url.path())
                if not ('EXIF:GPSLatitude' in exifData):
                    #May raise an error if no GPS data ?
                    exifData['EXIF:GPSLatitude'] = "0.0"
                    exifData['EXIF:GPSLongitude'] = "0.0"

                elem.set('latitude', str(exifData['EXIF:GPSLatitude']))
                elem.set('longitude', str(exifData['EXIF:GPSLongitude']))
        
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
        self.update_workspaces_model()
        print(ws)

    def open_workspace(self, directory_path, file_name):
        """ Open an existi ng workspace from a save file of the workspace.

        Args:
            directory_path (str): The absolute path of the directory containing the file.
            file_name (str): The name of the file containing the save of the workspace.
        """
        ws = Workspace.load(directory_path, file_name, Workspace)
        self.workspaces[ws.full_path()] = ws
        self.current_workspace = ws.full_path()
        self.update_workspaces_model()
        print("Workspace "+ws.full_path()+" successfully opened.")

    def close_workspace(self, workspace_path):
        """Close the workspace (it is not visible anymore in the list of open workspaces.
        Args:
            workspace_path (str): The absolute path of the workspace to close.
        """
        assert workspace_path in self.workspaces,\
                "The workspace " + workspace_path + " does not exists or is not opened."
        if self.current_workspace == workspace_path:
            self.current_workspace = ""
        del self.workspaces[workspace_path]
        self.update_workspaces_model()

    def change_workspace(self, workspace_path):
        """ Change the current workspace.

        Args:
            workspace_path (str): The absolute path of the workspace to select.
        """
        self.set_current_workspace(workspace_path)

    def save_workspace(self, workspace_path, file_name):
        """Save the workspace in a file.

        Args:
            workspace_path (str): The absolute path of the workspace to save.
            file_name (str): The name of the file to save into.
        """
        assert (workspace_path in self.workspaces),\
                "The workspace "+ workspace_path +" does not exist in the workspace manager."
        self.workspaces[workspace_path].save(file_name)

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
        self.update_workspaces_model()

    def update_workspaces_model(self):
        """ Updates the attribute workspaces_model.
        """
        self.workspaces_model.setStringList(list(self.workspaces.keys()))

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

    def change_scene(self, scene_path):
        """ Change the current scene identified by its path in the current workspace.

        Args:
            scene_path (str): The relative path of the scene to select in the current workspace.

        Raises:
            AssertionError: If the scene directory does not exist.
        """
        self.set_current_scene(scene_path)

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
            AssertionError: If the scene directory does not exist.
        """
        ws = self.get_current_workspace()
        ws.set_current_scene(scene_path)
