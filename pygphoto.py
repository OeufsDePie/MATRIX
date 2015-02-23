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

    # _files is an internal dictionnary that associate all the files present on the camera, along with their

    def __init__(self):
        self._files = []


    def _update_file_list(self, file_list):
        """Update the internal
        """
    
    def get_filename_list(self):
        """Generate the list of filenames for all the files present on the
        first camera found by requesting directly the camera.

        Raises a CalledProcessError when gphoto2 raised an error.

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
                filename = words[1]
                retval.append(filename)
        return retval

    def _get_filename(self, index):
        """Return the filename of the file indexed 'index' when listing all
        the files present on the camera

        Raises a CalledProcessError when gphoto2 raised an error.

        """
        # Show info on the file indexed 'index'
        command = [Pygphoto.GPHOTO, "--show-info", str(index)]
        output = subprocess.check_output(command)

        # The filename is the fourth word
        filename = output.split()[3]
        # We remove the trailing simple quotes ("'") 
        return filename.strip("'")
        

    def download_file(self, filename, output_dir):
        """Download the file name 'filename' and copy it to the given path.
        
        Returns 0 if succeeded. Returns 1 if the path is not an
        existing directory. Else returns the error code returned by
        gphoto.

        """
        print "\ndownload_file " + str(index) + " to " + str(output_dir) + "\n"
        # Check that the output dir is a valid directory
        if(not os.path.isdir(output_dir)):
            return 1
            
        # TODO check that the created file does not already exist...
        # This will save the file under "output_dir/filename.suffix"
        output_filepath = os.path.normpath(os.path.join(output_dir, "./%f.%C"))

        command = [Pygphoto.GPHOTO, "--get-file", str(index), "--filename", output_filepath]
        return subprocess.call(command)

    
    def download_files(self, filename_list, output_dir):
        """Download the whole list of files to the ouput directory

        This is equivalent to calling download_file on every file in
        the 'filename_list', but should be faster for a large number
        of files.

        """

if __name__ == "__main__":
    pygph = Pygphoto()
    print pygph._get_filename(1)
    # print pygph.get_filename_list()
    # print pygph.download_file(2, os.path.abspath("test/"))
    # print pygph.download_file(3, "test")
