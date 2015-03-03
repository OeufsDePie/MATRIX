import os
import json
from abc import abstractmethod
from Utils import Utils
from Serializable import Serializable

class Savable(Serializable):
    """ An object that can be saved and loaded in the file system.
    """

    @abstractmethod
    def save(self, base_path, file_name):
        """ Save the object in the file system.
        """
        # Serialize the object
        serial = self.serialize()
        # Get the full absolute name of the file
        assert os.path.isabs(base_path)
        file_name = Utils.valid_name(file_name)
        full_name = os.path.join(base_path,file_name)
        # Open the file in write mode
        with open(full_name,'w') as f:
            json.dump(serial,f)

    @classmethod
    @abstractmethod
    def load(cls, base_path, file_name, object_class):
        """ Recreate an object from the file

        Args:
            base_path (str): The path of the directory containing the file.
            file_name (str): The name of the file to load.
            object_class (class): The class of the object to recreate.
        """
        # Make sure base_path is an absolute path
        assert os.path.isabs(base_path), "The path "+base_path+" is not absolute."
        # Verifie that the file exists
        full_name = os.path.join(base_path,file_name)
        assert os.path.exists(full_name), "The file "+full_name+" does not exists."
        # Open and get the serialized version of the file
        with open(full_name,'r') as f:
            serial = json.load(f)
        # Return the deserialized version of the file
        return object_class.deserialize(serial)
