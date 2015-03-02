from DirectorySpace import DirectorySpace
from Utils import Utils
import os

class Scene(DirectorySpace):
    """ A scene containing all its images.

    Attributes:
        workspace (Workspace): The scene's workspace
        name (str): The name of the scene. It must be unique in the workspace.
            For example : "Shooting ENSEEIHT".
            Default is "scene_n" where n is the current number of scenes in workspace.
        relative_path (str): The path of the scene relatively to base_path.
    """

    def __init__(self, workspace, name="", relative_path=""):
        """ Initialize a scene in a workspace.

        Args:
            workspace (Workspace): The scene's workspace.
            name (str): The name of the scene.
            relative_path (str): The path relatively to the workspace.
        """
        self.workspace = workspace
        super().__init__(name,workspace.full_path(),relative_path)

    def delete(self):
        """ Delete the scene and remove its access from the workspace.

        It must not be called by itself but by the workspace !
        """
        super().delete()

    def __str__(self):
        """ Change displaying of a scene.

        Example:
            >>> print(scene)
        """
        s = ["Scene : " + self.name                       ,\
             "   workspace : " + self.workspace.name      ,\
             "   path      : " + self.relative_path]
        return "\n".join(s)
