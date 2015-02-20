#!/usr/bin/python3
import subprocess

class Pygphoto(object):
    """Allows simple operations on a USB connected camera.  

    This class allows to connect to a USB camera. List the names of
    the photos present in the camera and eventually download the
    photos individually.
    """

    # Command lines string value
    GPHOTO = "gphoto2"

    def __init__(self):
        pass
    
    def list_files():
        """Return the list of (filenumber, filename) couple for all the
        pictures present on the first camera found.

        """
        print "list_files"
        command[GPHOTO,""]
        call(command)
        
    def download_file(file_number, to_path):
        """Download the given file from the camera to the given path.

        """
        print "download_file " + str(file_number) + str(path)
