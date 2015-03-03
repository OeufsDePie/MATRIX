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
