import os
from PyQt5.QtCore import QDir
from Utils import Utils
from Serializable import Serializable       # need the package import in __init__.py

class DirectorySpace:
    """ A space based on a directory in the file system.

    Attributes:
        path_types (set(str)): A class attribute containing {"absolute","relative"}
        path_type (str): the type of the path ("absolute" or "relative")
        name (str): The name of the space.
        path (str): The path of the space.
        subdirs (dict(str,str)): The useful subdirectories (path,name).\
                The paths are the keys
        qt_directory (QDir): The directory corresponding to that workspace
    """
    path_types = frozenset(["absolute","relative"])

    def __init__(self, name="", absolute_path="", path_type="absolute"):
        """Initialize a DirectorySpace.

        Args:
            name (str): The name of the directory space. Default is "".
            absolute_path (str): The absolute path of the directory space. Default is "".
            path_type (str): "absolute" or "relative".\
                    It is the type of the string wich will be stored in the attribute path.\
                    It is NOT the type of the path given as an argument.\
                    This later one must be absolute.

        Raises:
            AssertionError: If a directory with that path already exists.
        """
        self.name = name
        absolute_path = Utils.valid_name(absolute_path)
        assert (os.path.isabs(absolute_path)), "The path " + absolute_path + " is not absolute."
        assert (path_type in self.path_types), "The type "+path_type+" does not exists." + \
                " Please use one in : " + self.path_types.__str__()
        self.qt_directory = QDir(absolute_path)
        assert (not self.qt_directory.exists()),\
                "The directory " + self.qt_directory.absolutePath() + " already exists. " + \
                "Please give a non-existing directory (it will be created)"
        assert (self.qt_directory.mkpath(".")), "The directory " +\
                self.qt_directory.absolutePath() + " can not be created."
        self.path_type = path_type
        if (path_type == "absolute"):
            self.path = self.qt_directory.absolutePath()
        else:
            self.path = self.qt_directory.dirName()
        self.subdirs = dict()

    def delete(self):
        """ Delete the directory space (and its contents).

        Raises:
            AssertionError: If the directory does not exist or can not be deleted.
        """
        # Deleting the workspace directory
        assert (self.qt_directory.exists()),\
                "The directory " + self.qt_directory.absolutePath() + " does not exists."
        assert (self.qt_directory.removeRecursively()),\
                "The directory " + self.qt_directory.absolutePath() + " can not be deleted."
