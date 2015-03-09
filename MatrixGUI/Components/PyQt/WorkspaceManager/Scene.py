from DirectorySpace import DirectorySpace
from Utils import Utils                     # need the package import in __init__.py
import os

class Scene(DirectorySpace):
    """ A scene containing all its images.

    Class Attributes:
        RECONSTRUCTION_OUTPUT_DIR
        RECONSTRUCTION_TEMP_DIR
        RECONSTRUCTION_PICTURE_DIR

    Attributes:
        name (str): The name of the scene. It must be unique in the workspace.
            For example : "Shooting ENSEEIHT".
            Default is "scene_n" where n is the current number of scenes in workspace.
        base_path (str): The path of the scene's workspace.
        relative_path (str): The path of the scene relatively to base_path.
        subdirs (dict(str,str)): The useful subdirectories (path,name).
    """
    RECONSTRUCTION_OUTPUT_DIR  = "reconstruction_output"
    RECONSTRUCTION_TEMP_DIR    = "reconstruction_temp"
    RECONSTRUCTION_PICTURE_DIR = "reconstruction_pictures"
    PICTURES_DIR               = "pictures_set"
    THUMBNAILS_DIR             = "thumbnails"

    def __init__(self, name, base_path, relative_path=""):
        """ Initialize a scene in a workspace.

        Args:
            name (str): The name of the scene.
            base_path (str): The path of the scene's workspace.
            relative_path (str): The path relatively to the workspace.
        """
        super().__init__(name,base_path,relative_path)
        self.subdirs[Scene.RECONSTRUCTION_OUTPUT_DIR] =\
                "The output directory for reconstruction"
        self.subdirs[Scene.RECONSTRUCTION_TEMP_DIR] =\
                "The temporary output directory for reconstruction"
        self.subdirs[Scene.RECONSTRUCTION_PICTURE_DIR] =\
                "The directory containing the pictures used for reconstruction"
        self.subdirs[Scene.THUMBNAILS_DIR] =\
                "The directory containing the thumbnails temporary stored when importing pictures"
        self.subdirs[Scene.PICTURES_DIR] =\
            "The directory holding all pictures files of the scene"

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


##############################   RECONSTRUCTION   ###################################

    def get_reconstruction_out_dir(self):
        return self.RECONSTRUCTION_OUTPUT_DIR

    def get_reconstruction_temp_dir(self):
        return self.RECONSTRUCTION_TEMP_DIR

    def get_reconstruction_picture_dir(self):
        return self.RECONSTRUCTION_PICTURE_DIR

#=============================   end reconstruction   ===============================

##############################   THUMBNAILS   ###################################
    def get_thumbnails_dir(self):
        return self.THUMBNAILS_DIR
#=============================   end thumbnails   ===============================
