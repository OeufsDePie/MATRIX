#!/usr/bin/python3
import subprocess
import os

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
    
    @staticmethod
    def list_files():
        """Return the list of (filenumber, filename) couple for all the
        pictures present on the first camera found.

        """
        print "\nlist_files\n"
        command = [Pygphoto.GPHOTO,"--list-files"]
        subprocess.call(command)


    @staticmethod
    def get_file(index, path):
        """Download the file numbered index and copy it to the given path.
        
        """
        print "\nget_file " + str(index) + " to " + str(path) + "\n"
        command = [Pygphoto.GPHOTO, "--get-file", str(index), "--filename", path]
        subprocess.call(command)

        
    def download_file(file_number, to_path):
        """Download the given file from the camera to the given path.

        """
        print "download_file " + str(file_number) + str(path)

    

if __name__ == "__main__":
    Pygphoto.list_files()
    Pygphoto.get_file(2, os.path.abspath("test/test2.jpg"))
    Pygphoto.get_file(3, "test/test3.png")

