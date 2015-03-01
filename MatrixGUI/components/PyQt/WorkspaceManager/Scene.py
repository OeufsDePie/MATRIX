from DirectorySpace import DirectorySpace
from Utils import Utils
import os

class Scene(DirectorySpace):
    """ A scene containing all its images.

    Attributes:
        workspace (Workspace): The workspace containing the scene.
        name (str): The name of the scene. It must be unique in the workspace.
            For example : "Shooting ENSEEIHT".
            Default is "scene_n" where n is the current number of scenes in workspace.
        path (str): The relative path of the scene.
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
        if not name:
            name = "scene_" + str(len(workspace.scenes)+1)
        path = Utils.valid_name(path)
        if not path:
            path = Utils.valid_name(name)
        super().__init__(name,os.path.join(workspace.path,path),"relative")

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
             "   path      : " + self.path]
        return "\n".join(s)
