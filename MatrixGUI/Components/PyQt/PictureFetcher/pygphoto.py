#!/usr/bin/python3
import re
import subprocess
import os
import time
import threading
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

class Pygphoto(QObject):
    """Allows simple operations on a USB connected camera by interfacing
    the gphoto2 command line tool.

    This class allows to interact with a USB camera. List the names of
    the photos present in the camera, watch for new files, and
    eventually download the photos individually.

    """
    # Constants
    # Command lines string value
    _GPHOTO = "gphoto2"
    # Camera events check period in seconds
    _EVENTS_PERIOD = 1

    # Signals
    onCameraConnection = pyqtSignal(bool)
    """This signal indicates if a camera is connected"""

    onContentChanged = pyqtSignal(list, list)
    """When watching the camera for new files, emit this signal when there
     has been some changes in the camera filesystem. Arguments are the
     lists of new files and deleted files
    """

    def __init__(self, watch_camera=False, watch_files=False):
        # _files_index is an internal dictionnary that associate all the
        # files present on the camera, along with their gphoto index
        self._files_index = dict()
        # _watching_files indicates if this component is watching for new files
        self._watching_files = watch_files
        # _watching_camera indicates if this component is watching for camera connections
        self._watching_camera = watch_camera
        # This lock is used to modify the watching flags
        self.__lock__ = threading.RLock()
        # Start the thread that watches for camera events
        self._watch_thread = threading.Thread(target=self._watch_events)
        self._watch_thread.daemon = True
        self._watch_thread.start()
        # The memorized state of camera connection
        self._camera_connection = False
        # The memorized occupied space on camera
        self._camera_occupied_space = 0
        
    def check_camera_connected(self):
        """Check if a camera is connected
        """
        # Try an auto-detect and see if there are results
        command = [Pygphoto._GPHOTO, "--auto-detect"]
        output = subprocess.check_output(command).decode("utf-8")
        lines = output.splitlines()
        # The first two lines are 
        # Model                          Port                                            
        # ----------------------------------------------------------
        # Then comes the list of connected camera (that can be empty)
        return (len(lines) > 2)

    def query_storage_info(self):
        """Return a dict of values concerny memory usage {free, occupied,
        total} containing values in KB

        """
        def first_int(string):
            # Take the first result of all the digit-only substrings
            return int(re.findall(r"\d+", string)[0])

        result = dict()
        command = [Pygphoto._GPHOTO, "--storage-info"]
        output = subprocess.check_output(command).decode("utf_8")
        output = output.splitlines()
        # Scan output for relevant information
        for line in output:
            if line.startswith("totalcapacity="):
                result["total"] = first_int(line)
            elif line.startswith("free="):
                result["free"] = first_int(line)
        # Compute occupied value
        result["occupied"] = result["total"] - result["free"]
        return result

    def _update_file_list(self, filenames_list):
        """Update the internal dictionnary of filenames

        """
        with self.__lock__:
            # Number each files, starting with 1
            self._files_index = dict(zip(filenames_list,
                                         range(1, len(filenames_list) + 1)))

    def _query_filename(self, index):
        """Return the filename of the file indexed "index" when listing all
        the files present on the camera

        Raises a CalledProcessError when gphoto2 raised an error.

        """
        # Show info on the file indexed "index"
        command = [Pygphoto._GPHOTO, "--show-info", str(index)]
        output = subprocess.check_output(command).decode("utf-8")

        # The filename is the fourth word
        filename = output.split()[3]
        # We remove the trailing simple quotes ("'")
        return filename.strip("'")

    def query_file_list(self):
        """Generate the list of filenames for all the files present on the
        first camera found by requesting directly the camera.

        Raises a CalledProcessError when gphoto2 raised an error.

        """
        retval = []  # Result list of filenames

        # Grab the output of the list file command
        command = [Pygphoto._GPHOTO,"--list-files"]
        output = subprocess.check_output(command).decode("utf-8")

        # Parse the output for "#" lines
        for line in iter(output.splitlines()):
            if line[0] == "#":
                # Split every one or more whitespaces
                words = line.split()
                filename = words[1]
                retval.append(filename)

        # Take the opportunity to update the internal file list
        # and return
        self._update_file_list(retval)
        return retval

    def download_file(self, filename, output_dir, overwrite=True, thumbnail=False):
        """Download the file name "filename" and copy it to the given path.

        Returns 0 if succeeded. Else returns the error code returned by
        gphoto.

        """
        # Check that the output dir is a valid directory
        assert(os.path.isdir(output_dir))

        with self.__lock__:
            # Get the gphoto index of the file and check it is up to date
            index = self._files_index[filename]
            if (not self._query_filename(index) == filename):
                # Update the files dictionnary
                self.query_file_list()
                index = self._files_index[filename]

        # The destination is "output_dir/filename
        destination_path = os.path.normpath(os.path.join(output_dir, filename))

        # Check that the file does not already exist
        if(os.path.exists(destination_path)):
            if(overwrite):
                # First remove the file
                os.remove(destination_path)
            else:
                # Do nothing
                return 0

        # Determine the command name
        if(thumbnail):
            command = "--get-thumbnail"
        else:
            command = "--get-file"
        command_line = [Pygphoto._GPHOTO,
                   command, str(index),
                   "--filename", destination_path]
        return subprocess.call(command_line)

    def download_files(self, filename_list, output_dir, overwrite=True, thumbnail=False):
        """Download the whole list of files to the ouput directory

        Return 0 if all the files were downloaded, 1 if
        there was a problem for one of the files.

        This is equivalent to calling download_file on every file in
        the "filename_list", but should be faster for a large number
        of files.

        """
        # Check that the output dir is a valid directory
        assert(os.path.isdir(output_dir))

        # Determine the command name
        if(thumbnail):
            command = "--get-thumbnail"
        else:
            command = "--get-file"

        # Update the files dictionnary
        self.query_file_list()

        print(filename_list)
        with self.__lock__:
            # Download each file
            for filename in filename_list:
                index = self._files_index[filename]
                # The destination is "output_dir/filename
                destination_path = os.path.normpath(os.path.join(output_dir, filename))
                command_line = [Pygphoto._GPHOTO,
                           command, str(index),
                           "--filename", destination_path]
                # Check that the file does not already exist
                if(os.path.exists(destination_path)):
                    if(overwrite):
                        # First remove the file
                        os.remove(destination_path)
                    else:
                        # Do nothing
                        continue
                return_code = subprocess.call(command_line)
                if(return_code != 0):
                    return return_code
        return 0

    def download_all(self, output_dir, overwrite=True, thumbnail=False):
        """Download all the files present on the camera.

        Overwrites preexisting files. Faster than 'download_files()'.

        """
        # Check that the output dir is a valid directory
        assert(os.path.isdir(output_dir))
        # The destination is "output_dir/filename.suffix
        destination_path = os.path.normpath(os.path.join(output_dir, "%f.%C"))

        if(thumbnail):
            command = "--get-all-thumbnails"
        else:
            command = "--get-all-files"
        command_line = [Pygphoto._GPHOTO,
                   command,
                   "--filename",
                   destination_path]
        if(overwrite):
            command_line.append("--force-overwrite")
        return subprocess.call(command_line)

    ###############################
    #  Watching functionality     #
    ###############################
    
    def set_watching_files(self, value):
        """Set whether the component should watch for changes in the camera
        filesystem.

        """
        with self.__lock__:
            self._watching_files = value

    def set_watching_camera(self, value):
        """Set whether the component should watch for presence of a connected
        camera.

        """
        with self.__lock__:
            self._watching_camera = value
 
    def is_watching_file(self, value):
        """Indicates whether the component is watching for changes in the camera
        filesystem.

        """
        with self.__lock__:
            return self._watching_files

    def is_watching_camera(self, value):
        """Indicates whether the component is watching for presence of a connected
        camera.

        """
        with self.__lock__:
            return self._watching_camera
 

    def _watch_events(self):
        """Executed by the watching thread : checks for every events.
        """
        while(True):
            with self.__lock__:
                if self._watching_camera:
                    self._watch_camera()
                if (self._watching_files 
                    and self._camera_connection):
                    self._watch_files()
            time.sleep(Pygphoto._EVENTS_PERIOD)

    def _watch_camera(self):
        """Check for a change in camera connection, possibly raising a
        onCameraConnection signal.

        """
        new_camera_connection = self.check_camera_connected()
        if(new_camera_connection != self._camera_connection):
            # Raise a signal
            Pygphoto.onCameraConnection.emit(new_camera_connection)
        # Set new state
        self._camera_connection = new_camera_connection

    def _watch_files(self):
        """Check for changes in the camera filesystem, possibly raising a
        onContentChanged signal.

        """
        new_occupied_space = self.query_storage_info()
        if(new_occupied_space != self._camera_occupied_space):
            # Search for new and deleted files
            diff = self._diff_files()
            # Raise a signal
            Pygphoto.onContentChanged.emit(diff)
        # Set new state
        self._camera_occupied_space = new_occupied_space
        
    def _diff_files(self):
        """Query the camera and return the couple of lists (new_files,
        deleted_files) relatively to the last check.

        """
        new_files = []
        deleted_files = []
        # Copy last index
        with self.__lock__:
            last_files_index = self._files_index.copy()
        # Update index
        self.query_file_list()
        # Copy recent index
        with self.__lock__:
            recent_files_index = self._files_index.copy()

        # Check for new files
        for recent_file in recent_files_index:
            # Check recent_files was already present
            if not(recent_file in last_files_index):
                new_files.append(recent_file)
        # Check for deleted files
        for last_file in last_files_index:
            # Check last_files is still present
            if not(last_file in recent_files_index):
                deleted_files.append(last_file)

        return (new_files, deleted_files)

if __name__ == "__main__":
    # TESTINGS
    pygph = Pygphoto(watch_camera=True, watch_files=False)

    class TestPygphoto(QObject):
        @pyqtSlot(bool)
        def connectCamera():
            pass

    # Wait for a camera to connect
    print("Waiting for connected camera...")
    while True:
        if pygph.check_camera_connected():
            break
        time.sleep(0.5)

    # print("\n~~~~~~~~ _query_filename")
    # filename = pygph._query_filename(1)
    # print(filename)
    # print("\n~~~~~~~~ _query_file_list")
    # filelist = pygph.query_file_list()
    # print("\n~~~~~~~~ download_file False")
    # print(pygph.download_file(filename, "test", overwrite=False))
    # print("\n~~~~~~~~ download_file False")
    # print(pygph.download_file(filename, "test", overwrite=False))
    # print("\n~~~~~~~~ download_file True")
    # print(pygph.download_file(filename, "test", overwrite=True))
    # print("\n~~~~~~~~ download_all_thumbnails")
    # print(pygph.download_all("thumbnails", thumbnail=True))
    # print("\n~~~~~~~~ download_files False")
    # print(pygph.download_files(filelist, "test", overwrite=False))
    # print("\n~~~~~~~~ download_all")
    # print(pygph.download_all("test"))

    input("\n~~~~~~~~ Waiting for events now. Press Return to disable watching.")
    pygph.set_watching_camera(False)
    pygph.set_watching_files(False)
    input("\n~~~~~~~~ Watching disabled. Press Return to end.")
    
