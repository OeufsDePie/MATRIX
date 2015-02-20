from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

class ICamera(QObject):
    
    # This signal indicate if a camera is connected, if so it provide
    # with the port it is connected to
    cameraConnectionSignal = pyqtSignal(bool,str)

    # When a new photo is available
    newPhotoSignal = pyqtSignal(int)

    def __init__(self,pathPly,pathPictures):
        QObject.__init__(self)
    
    @pyqtSlot()
    def download_file(self, file_number):
	pass
