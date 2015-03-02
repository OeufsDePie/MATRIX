from DirectorySpace import DirectorySpace
from Utils import Utils                     # need the package import in __init__.py
import os

class Scene(DirectorySpace):
    """ A scene containing all its images.

    Attributes:
        name (str): The name of the scene. It must be unique in the workspace.
            For example : "Shooting ENSEEIHT".
            Default is "scene_n" where n is the current number of scenes in workspace.
        base_path (str): The path of the scene's workspace.
        relative_path (str): The path of the scene relatively to base_path.
    """

    def __init__(self, name, base_path, relative_path=""):
        """ Initialize a scene in a workspace.

        Args:
            name (str): The name of the scene.
            base_path (str): The path of the scene's workspace.
            relative_path (str): The path relatively to the workspace.
        """
        super().__init__(name,base_path,relative_path)

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
             "   workspace : " + self.base_path           ,\
             "   path      : " + self.relative_path]
        return "\n".join(s)

    @staticmethod
    def deserialize(serial):
        """ Regenerate a Scene object from serialized data (JSON like).

        Args:
            serial (dict()): The serialized version of a Scene object.
        """
        scene = DirectorySpace.deserialize(serial)
        scene.__class__ = Scene
        return scene
