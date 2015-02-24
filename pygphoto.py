#!/usr/bin/python3
import subprocess
import os

class Pygphoto(object):
    '''Allows simple operations on a USB connected camera by interfacing
    the gphoto2 command line tool.

    This class allows to connect to a USB camera. List the names of
    the photos present in the camera and eventually download the
    photos individually.

    '''

    # Command lines string value
    GPHOTO = 'gphoto2'

    def __init__(self):
        # _files is an internal dictionnary that associate all the
        # files present on the camera, along with their
        self._files = {}


    def _update_file_list(self, filenames_list):
        '''Update the internal dictionnary of filenames

        '''
        # Number each files, starting with 1
        self._files = dict(zip(filenames_list, range(1,len(filenames_list) + 1)));
    
    def _query_filename(self, index):
        '''Return the filename of the file indexed 'index' when listing all
        the files present on the camera

        Raises a CalledProcessError when gphoto2 raised an error.

        '''
        # Show info on the file indexed 'index'
        command = [Pygphoto.GPHOTO, '--show-info', str(index)]
        output = subprocess.check_output(command)

        # The filename is the fourth word
        filename = output.split()[3]
        # We remove the trailing simple quotes ("'") 
        return filename.strip("'")

     def query_file_list(self):
        '''Generate the list of filenames for all the files present on the
        first camera found by requesting directly the camera.

        Raises a CalledProcessError when gphoto2 raised an error.

        '''
        retval = [] # Result list of filenames

        # Grab the output of the list file command
        command = [Pygphoto.GPHOTO,'--list-files']
        output = subprocess.check_output(command) 

        # Parse the output for '#' lines
        for line in iter(output.splitlines()):
            if line[0] == '#':
                # Split every one or more whitespaces
                words = line.split()
                filename = words[1]
                retval.append(filename)

        # Take the opportunity to update the internal file list
        # and return
        self._update_file_list(retval)
        return retval

    def download_file(self, filename, output_dir, overwrite=True):
        '''Download the file name 'filename' and copy it to the given path.
        
        Returns 0 if succeeded. Returns 1 if the path is not an
        existing directory. Else returns the error code returned by
        gphoto.

        '''
        # Check that the output dir is a valid directory
        if(not os.path.isdir(output_dir)):
            return 1

        # Get the gphoto index of the file and check it is up to date
        index = self._files[filename]
        if (not self._query_filename(index) == filename):
            # Update the files dictionnary
            self.query_file_list()
            index = self._files[filename]

        # The destination is 'output_dir/filename
        destination_path = os.path.normpath(os.path.join(output_dir, filename))

        # Check that the file does not already exist
        if(os.path.exists(destination_path)):
            if(overwrite):
                # First remove the file
                os.remove(destination_path)
            else:
                # Do nothing
                return 0

        command = [Pygphoto.GPHOTO, '--get-file', str(index), '--filename', destination_path]
        return subprocess.call(command)

    
    def download_files(self, filename_list, output_dir, overwrite=True):
        '''Download the whole list of files to the ouput directory

        Return 0 if all the files were downloaded, 1 if
        there was a problem for one of the files or if the output_dir
        is not a valid directory

        This is equivalent to calling download_file on every file in
        the 'filename_list', but should be faster for a large number
        of files.

        '''
        # Check that the output dir is a valid directory
        if(not os.path.isdir(output_dir)):
            return 1

        # Update the files dictionnary
        self.query_file_list()

        # Download each file
        for filename in filename_list:
            index = self._files[filename]
            # The destination is 'output_dir/filename
            destination_path = os.path.normpath(os.path.join(output_dir, filename))
            command = [Pygphoto.GPHOTO, '--get-file', str(index), '--filename', destination_path]
            # Check that the file does not already exist
            if(os.path.exists(destination_path)):
                if(overwrite):
                    # First remove the file
                    os.remove(destination_path)
                else:
                    # Do nothing
                    continue
            return_code = subprocess.call(command)
            if(return_code != 0):
                return return_code
                
        return 0
        
    def download_all(self, output_dir):
        '''Download all the files present on the camera

        Careful : overwrites
        Faster than 'download_files()'
        '''
        # Check that the output dir is a valid directory
        if(not os.path.isdir(output_dir)):
            return 1
        # The destination is 'output_dir/filename.suffix
        destination_path = os.path.normpath(os.path.join(output_dir, '%f.%C'))

        command = [Pygphoto.GPHOTO, '--get-all-files', '--filename', destination_path]
        command.append('--force-overwrite')
        return subprocess.call(command)

        
if __name__ == '__main__':
    # TESTINGS
    pygph = Pygphoto()
    
    print '~~~~~~~~ _query_filename'
    filename = pygph._query_filename(1)
    print filename
    print '~~~~~~~~ _query_file_list'
    filelist = pygph.query_file_list()
    print '~~~~~~~~ download_file False'
    print pygph.download_file(filename, os.path.abspath('test/'), overwrite=False)
    print '~~~~~~~~ download_file False'
    print pygph.download_file(filename, os.path.abspath('test/'), overwrite=False)
    print '~~~~~~~~ download_file True'
    print pygph.download_file(filename, os.path.abspath('test/'), overwrite=True)
    print '~~~~~~~~ download_files False'
    print pygph.download_files(filelist, os.path.abspath('test/'), overwrite=False)
    print '~~~~~~~~ download_all'
    print pygph.download_all(os.path.abspath('test/'))
    # print pygph.download_file(3, 'test')
