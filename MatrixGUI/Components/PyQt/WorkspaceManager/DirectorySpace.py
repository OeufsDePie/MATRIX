import os
from PyQt5.QtCore import QDir
from Utils import Utils                     # need the package import in __init__.py
from Savable import Savable                 # need the package import in __init__.py

class DirectorySpace(Savable):
    """ A space based on a directory in the file system.

    Attributes:
        name (str): The name of the space.
        base_path (str): The absolute path of the directory containing the space.
        relative_path (str): The path of the directory space relatively to base_path.
        subdirs (dict(str,str)): The useful subdirectories (path,name).\
                The paths are the keys
        qt_directory (QDir): The directory corresponding to that workspace
    """

    def __init__(self, name="", base_path="", relative_path=""):
        """Initialize a DirectorySpace.

        Args:
            name (str): The name of the directory space. Default is "".
            base_path (str): The absolute path of the directory containing the space.
            relative_path (str): The path of the space relatively to base_path.

        Raises:
            AssertionError: If a directory with that path already exists.
        """
        assert name, "The argument name must not be empty"
        self.name = name
        base_path = Utils.valid_name(base_path)
        self.base_path = base_path
        relative_path = Utils.valid_name(relative_path)
        if not relative_path:
            relative_path = Utils.valid_name(name)
        self.relative_path = relative_path
        assert (os.path.isabs(base_path)), "The path " + base_path + " is not absolute."
        self.qt_directory = QDir(os.path.join(base_path,relative_path))
        self.subdirs = dict()

    def create_directory(self):
        """ Effectively creates the directory thanks to Qt object QDir
        """
        assert (not self.qt_directory.exists()),\
                "The directory " + self.qt_directory.absolutePath() + " already exists. " + \
                "Please give a non-existing directory (it will be created)"
        assert (self.qt_directory.mkpath(".")), "The directory " +\
                self.qt_directory.absolutePath() + " can not be created."
        for subpath in self.subdirs:
            self.qt_directory.mkpath(subpath)

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

    def full_path(self):
        return os.path.join(self.base_path, self.relative_path)

    def serialize(self):
        return dict(\
                name = self.name,\
                base_path = self.base_path,\
                relative_path = self.relative_path)


    @staticmethod
    def deserialize(serial):
        return DirectorySpace(\
                name=serial['name'],\
                base_path=serial['base_path'],\
                relative_path=serial['relative_path'])

    def save(self, file_name):
        """ Save the object in the file system.
        """
        # path of the directory containing the the save
        directory_path = self.full_path()
        super().save(directory_path,file_name)

    @classmethod
    def load(cls, base_path, file_name, object_class=None):
        """ Recreate a DirectorySpace object from a file.

        Args:
            base_path (str): The path of the directory containing the file.
            file_name (str): The name of the file to load.
            object_class (class): The class of the object to recreate.
        """
        if object_class == None:
            object_class = cls
        return Savable.load(base_path, file_name, object_class)
