#!/usr/bin/python3
import re
import subprocess
import os
import threading
import sys
from PyQt5.QtCore import QObject
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot

class Pygphoto(QObject):
    """Allows simple operations on a USB connected camera by interfacing
    the gphoto2 command line tool.

    This class allows to interact with a USB camera. List the names of
    the photos present in the camera, watch for new files, and
    eventually download the photos individually.  Needs a QApplication
    to be instantiated in order to watch properly for events.

    """
    # Constants
    # Command lines string value
    _GPHOTO = "gphoto2"

    # Camera events check period in milliseconds
    _EVENTS_PERIOD = 500

    # Signals
    onCameraConnection = pyqtSignal(bool)
    """This signal indicates if a camera is connected"""

    onContentChanged = pyqtSignal(list, list)
    """When watching the camera for new files, emit this signal when there
    has been some changes in the camera filesystem. Arguments are the
    lists of new files and deleted files
    """

    _onWatchCamera = pyqtSignal(bool)
    """This signal indicates if the component should start or stop
    watching for connection events with a camera."""

    _onWatchFile = pyqtSignal(bool)
    """This signal indicates if the component should start or stop
    watching for new files on the camera."""

    def __init__(self, watch_camera=False, watch_files=False):
        # Super constructor
        QObject.__init__(self)
        # _files_index is an internal dictionnary that associate all the
        # files present on the camera, along with their gphoto index
        self._files_index = dict()
        # Create mutex for the camera
        self._camera_lock = threading.Lock()
        # Create an internal CameraWatcher
        self._camera_watcher = Pygphoto.CameraWatcher(self, watch_camera, watch_files)
        # Connect watch file and watch camera signals
        self._onWatchFile.connect(self._camera_watcher.set_watching_files)
        self._onWatchCamera.connect(self._camera_watcher.set_watching_camera)
        # Forward signals from camera_watcher
        self._camera_watcher.onCameraConnection.connect(self.__forward_onCameraConnection)
        self._camera_watcher.onContentChanged.connect(self.__forward_onContentChanged)
        # Create a thread to execute the CameraWatcher in
        self._watcher_thread = QThread()
        self._camera_watcher.moveToThread(self._watcher_thread)
        # Start the watching
        self._watcher_thread.started.connect(self._camera_watcher._watch_events)
        self._watcher_thread.start()

    def check_camera_connected(self):
        """Check if a camera is connected.

        Raises a CalledProcessError when gphoto2 raised an error.
        """
        # Try an auto-detect and see if there are results
        command = [Pygphoto._GPHOTO, "--auto-detect"]
        with self._camera_lock:
            output = subprocess.check_output(command).decode("utf-8")
        lines = output.splitlines()
        # The first two lines are 
        # Model                          Port                                            
        # ----------------------------------------------------------
        # Then comes the list of connected camera (that can be empty)
        return (len(lines) > 2)

    def query_camera_name(self):
        """Return the camera name, or unknown.
        """
        result = "Unknown"
        model_string = "Model: "
        command = [Pygphoto._GPHOTO, "--summary"]
        try:
            with self._camera_lock:
                output = subprocess.check_output(command).decode("utf-8")
            lines = output.splitlines()
            for line in lines:
                if line.startswith(model_string):
                    # The name follows the model_string
                    result = line[len(model_string):] 
        except subprocess.CalledProcessError:
            pass
        return result

    def query_storage_info(self):
        """Return a dict of values concerny memory usage {free, occupied,
        total} containing values in KB.

        Raises a CalledProcessError when gphoto2 raised an error.

        """
        def first_int(string):
            # Take the first result of all the digit-only substrings
            return int(re.findall(r"\d+", string)[0])

        result = dict()
        command = [Pygphoto._GPHOTO, "--storage-info"]
        with self._camera_lock:
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

    def _filelist_to_dict(filenames_list):
        """Convert a filename list to a dictionnary associating filenames
        with their index.

        """
        # Number each files, starting with 1
        return dict(zip(filenames_list, range(1, len(filenames_list) + 1)))
        
    def _query_filename(self, index):
        """Return the filename of the file indexed "index" when listing all
        the files present on the camera

        Raises a CalledProcessError when gphoto2 raised an error.

        """
        # Show info on the file indexed "index"
        command = [Pygphoto._GPHOTO, "--show-info", str(index)]
        with self._camera_lock:
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
        with self._camera_lock:
            output = subprocess.check_output(command).decode("utf-8")

        # Parse the output for "#" lines
        for line in iter(output.splitlines()):
            if line[0] == "#":
                # Split every one or more whitespaces
                words = line.split()
                filename = words[1]
                retval.append(filename)

        return retval

    def download_file(self, filename, output_dir, overwrite=True, thumbnail=False):
        """Download the file name "filename" and copy it to the given path.

        Returns 0 if succeeded. Else returns the error code returned by
        gphoto.

        """
        # Check that the output dir is a valid directory
        assert(os.path.isdir(output_dir))

        # Get the gphoto index of the file and check it is up to date
        if(not filename in self._files_index
           or not self._query_filename(self._files_index[filename]) == filename):
            # Update the files dictionnary
            self._files_index = Pygphoto._filelist_to_dict(self.query_file_list())

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
        with self._camera_lock:
            return_code = subprocess.call(command_line)
        return return_code

    def download_files(self, filename_list, output_dir, overwrite=True, thumbnail=False):
        """Download the whole list of files to the ouput directory

        Return the paths list of downloaded files. This is equivalent
        to calling download_file on every file in the "filename_list",
        but should be faster for a large number of files.

        """
        # Check that the output dir is a valid directory
        assert(os.path.isdir(output_dir))

        # Init the result list
        result = []

        # Determine the command name
        if(thumbnail):
            command = "--get-thumbnail"
        else:
            command = "--get-file"

        # Update the files dictionnary
        self._files_index = Pygphoto._filelist_to_dict(self.query_file_list())

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
            with self._camera_lock:
                return_code = subprocess.call(command_line)
            if(return_code == 0):
                result.append(destination_path)
        return result

    def download_all(self, output_dir, overwrite=True, thumbnail=False):
        """Download all the files present on the camera.

        Overwrites preexisting files. Faster than 'download_files()'.
        Return the return code returned by the gphoto call

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
        with self._camera_lock:
            return_code = subprocess.call(command_line)
        return return_code

    ###############################
    #  Watching functionality     #
    ###############################

    # If we want to forward signals
    @pyqtSlot(bool)
    def __forward_onCameraConnection(self, boolean):
        self.onCameraConnection.emit(boolean)

    @pyqtSlot(list, list)
    def __forward_onContentChanged(self, newfiles, delfiles):
        self.onContentChanged.emit(newfiles, delfiles)

    @pyqtSlot(bool)
    def set_watching_files(self, value):
        """Set whether the component should watch for changes in the camera
        filesystem.

        """
        self._onWatchFile.emit(value)

    @pyqtSlot(bool)
    def set_watching_camera(self, value):
        """Set whether the component should watch for presence of a connected
        camera.

        """
        self._onWatchCamera.emit(value)

    class CameraWatcher(QObject):

        # Signals
        onCameraConnection = pyqtSignal(bool)
        """This signal indicates if a camera is connected"""

        onContentChanged = pyqtSignal(list, list)
        """When watching the camera for new files, emit this signal when there
        has been some changes in the camera filesystem. Arguments are
        the lists of new files and deleted files

        """

        def __init__(self, pygphoto, watch_camera, watch_files):
            # Super constructor
            QObject.__init__(self)
            # The reference to the gphoto instance to use
            self.__pygph = pygphoto
            # _files_index is an internal dictionnary that associate
            # all the files present on the camera, along with their
            # gphoto index
            self._files_index = dict()
            # Internal lock for accessing some of the attributes
            self.__lock__ = threading.RLock()
            # _watching_files indicates if this component is watching for new files
            self._watching_files = watch_files
            # _watching_camera indicates if this component is watching for camera connections
            self._watching_camera = watch_camera
            # The memorized state of camera connection
            self._camera_connection = False
            # The memorized occupied space on camera
            self._camera_occupied_space = 0

        @pyqtSlot(bool)
        def set_watching_files(self, value):
            """Set whether the component should watch for changes in the camera
            filesystem.

            """
            print("Set watching files: " + str(value))
            with self.__lock__:
                self._watching_files = value

        @pyqtSlot(bool)
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

        @pyqtSlot()
        def _watch_events(self):
            """Executed by the watching thread : checks for every events.
            """
            # Check for the different events
            with self.__lock__:
                if self._watching_camera:
                    self._watch_camera()
                if (self._watching_files 
                    and self._camera_connection):
                    self._watch_files()
            # Non blocking 'recursive' call
            QTimer.singleShot(Pygphoto._EVENTS_PERIOD, self._watch_events)

        def _watch_camera(self):
            """Check for a change in camera connection, possibly raising a
            onCameraConnection signal.

            """
            new_camera_connection = self.__pygph.check_camera_connected()
            if(new_camera_connection != self._camera_connection):
                # Raise a signal
                self.onCameraConnection.emit(new_camera_connection)
            # Set new state
            self._camera_connection = new_camera_connection

        def _watch_files(self):
            """Check for changes in the camera filesystem, possibly raising a
            onContentChanged signal.

            """
            try:
                new_occupied_space = self.__pygph.query_storage_info()
                if(new_occupied_space != self._camera_occupied_space):
                    # Search for new and deleted files
                    diff = self._diff_files()
                    # Check there are actually some changes
                    if(diff[0] or diff[1]):
                        # Raise a signal
                        self.onContentChanged.emit(diff[0], diff[1])
                # Set new state
                self._camera_occupied_space = new_occupied_space
            except subprocess.CalledProcessError:
                pass

        def _diff_files(self):
            """Query the camera and return the couple of lists (new_files,
            deleted_files) relatively to the last check.

            """
            new_files = []
            deleted_files = []
            # Copy last index
            last_files_index = self._files_index.copy()
            # Update index
            self._files_index = Pygphoto._filelist_to_dict(self.__pygph.query_file_list())

            # Check for new files
            for recent_file in self._files_index:
                # Check recent_files was already present
                if not(recent_file in last_files_index):
                    new_files.append(recent_file)
            # Check for deleted files
            for last_file in last_files_index:
                # Check last_files is still present
                if not(last_file in self._files_index):
                    deleted_files.append(last_file)

            return (new_files, deleted_files)

if __name__ == "__main__":
    # TESTINGS
    from PyQt5.QtWidgets import QApplication

    class TestPygphoto(QObject):
        def __init__(self):
            QObject.__init__(self)

        @pyqtSlot(bool)
        def connectCamera(self, boolean):
            print("Camera connected : " + str(boolean))

        @pyqtSlot(list, list)
        def newFiles(self, new, deleted):
            print("New files : " + str(new))
            print("Deleted files : " + str(deleted))

    app = QApplication(sys.argv)

    testpygph = TestPygphoto()
    pygph = Pygphoto(watch_camera=True, watch_files=True)
    pygph.onCameraConnection.connect(testpygph.connectCamera)
    pygph.onContentChanged.connect(testpygph.newFiles)
    print("\n~~~~~~~~ query_camera_name")
    print(pygph.query_camera_name())
    print("\n~~~~~~~~ _query_filename")
    filename = pygph._query_filename(1)
    print(filename)
    print("\n~~~~~~~~ _query_file_list")
    filelist = pygph.query_file_list()
    print("\n~~~~~~~~ download_file False")
    print(pygph.download_file(filename, "test", overwrite=False))
    print("\n~~~~~~~~ download_file False")
    print(pygph.download_file(filename, "test", overwrite=False))
    print("\n~~~~~~~~ download_file True")
    print(pygph.download_file(filename, "test", overwrite=True))
    print("\n~~~~~~~~ download_all_thumbnails")
    print(pygph.download_all("thumbnails", thumbnail=True))
    print("\n~~~~~~~~ download_files False")
    print(pygph.download_files(filelist, "test", overwrite=False))
    print("\n~~~~~~~~ download_all")
    print(pygph.download_all("test"))

    input("Waiting for events now. Press Return to disable watching.\n\n")
    pygph.set_watching_camera(False)
    pygph.set_watching_files(False)
    input("Watching disabled. Press Return to end.\n\n")
    
