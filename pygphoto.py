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
        """Returns the list of (filenumber, filenames) for all the files
        present on the first camera found.

        Raises a CalledProcessError when gphoto2 raised an error.  The
        filenumber correspond to the index of the corresponding file
        in the file list printed by gphoto. This filenumber is needed
        when downloading a file from the camera.

        """
        print "\nlist_files\n"
        retval = [] # Result list of filenames

        # Grab the output of the list file command
        command = [Pygphoto.GPHOTO,"--list-files"]
        output = subprocess.check_output(command) 

        # Parse the output for '#' lines
        for line in iter(output.splitlines()):
            if line[0] == "#":
                # Split every one or more whitespaces
                words = line.split()
                filenumber = int(words[0][1:]) # remove '#'
                filename = words[1]
                retval.append((filenumber, filename))
        return retval


    @staticmethod
    def download_file(index, path):
        """Download the file numbered index and copy it to the given path.
        Returns 0 if succeeded. Else returns the error code returned by gphoto.
        """
        print "\ndownload_file " + str(index) + " to " + str(path) + "\n"
        command = [Pygphoto.GPHOTO, "--get-file", str(index), "--filename", path]
        return subprocess.call(command)

        
if __name__ == "__main__":
    print Pygphoto.list_files()
    print Pygphoto.download_file(2, os.path.abspath("test/test2.jpg"))
    print Pygphoto.download_file(3, "test/test3.jpg")
