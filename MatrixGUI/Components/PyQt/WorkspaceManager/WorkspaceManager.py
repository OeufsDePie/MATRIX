import os, random, math
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
        scenes_model (QStringListModel): The list model (for qml) of the scenes in the current workspace.
    """
    def __init__(self):
        """Initialize a workspace manager.
        """
        self.workspaces = dict()
        self.current_workspace = "" 
        self.workspaces_model = QStringListModel()
        self.scenes_model = QStringListModel()

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

##############################   WORKSPACE   ###################################

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
        self.update_scenes_model()

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
        self.update_scenes_model()

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
        self.update_scenes_model()

#=============================   end workspace   ===========================

##############################   SCENE   ###################################

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
        self.update_scenes_model()

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
        self.update_scenes_model()

    def get_current_scene(self):
        return self.get_current_workspace().get_current_scene()

    def set_current_scene(self, scene_path):
        """ Change the current scene identified by its path in the current workspace.

        Args:
            scene_path (str): The relative path of the scene to select in the current workspace.

        Raises:
            AssertionError: If the scene directory does not exist.
        """
        ws = self.get_current_workspace()
        ws.set_current_scene(scene_path)

    def update_scenes_model(self):
        """ Updates the attribute scenes_model.
        """
        if not self.current_workspace:
            scenes_list = list()
        else:
            scenes_list = list(self.get_current_workspace().scenes.keys())
        self.scenes_model.setStringList(scenes_list)

    def get_scene_output_dir(self):
        """ Returns the absolute path of the output directory for ply files.

        Returns:
            str: The absolute path of directory.
        """
        return os.path.join(\
                self.get_current_scene().full_path(),\
                self.get_current_scene().get_reconstruction_out_dir())

    def get_scene_temp_output_dir(self):
        """ Returns the temporary output directory for scene reconstructions.

        Returns:
            str: The absolute path of the temporary directory.
        """
        return os.path.join(\
                self.get_current_scene().full_path(),\
                self.get_current_scene().get_reconstruction_temp_dir())

    def get_selected_picture_dir(self):
        """ Returns the absolute path of the directory containing the pictures used for reconstruction.

        Returns:
            str: The absolute path of the picture directory.
        """
        return os.path.join(\
                self.get_current_scene().full_path(),\
                self.get_current_scene().get_reconstruction_picture_dir())

    def import_pictures(self, picturesFiles):
        #Temporary, waiting for you matpiz <3
        return picturesFiles

    def get_thumbnails_dir(self):
        #Temporary, waiting for you matpiz <3
        return os.path.join(\
            self.get_current_scene().full_path(),\
            self.get_current_scene().get_thumbnails_dir())

#=============================   end scene   ===========================
