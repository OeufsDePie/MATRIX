#! /usr/bin/python3
#import interfaceReconstruction
import sys, signal, os
#from OpenGL import GL
from PyQt5.QtQuick import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtQml import *
from components.PyQt.PictureManager.pictureManager import *
from components.PyQt.WorkspaceManager.workspaceManager import *
from components.PyQt.PictureFetcher.pictureFetcher import *

class Orchestrator(QObject):
  MAIN_VIEW = os.path.join(os.getcwd(), "MainWindow.qml")
  QML_PACKAGE = os.path.join(os.getcwd(), "Components", "QML")
  RESOURCES = os.path.join(os.getcwd(), "Resources")

  # Define all sendable signals
  # Send to inform view that picture has been moved  
  pictureMoved = pyqtSignal(int)
  # Send to inform that pictures have been filtered
  picturesFiltered = pyqtSignal()
  # Send to inform that picture have been imported. 
  picturesImported = pyqtSignal(QVariant)

  # Define All Usable Slots
  @pyqtSlot(int, int)
  def movePicture(self, indexFrom, indexTo):
    """
      A slot that handle the reorganization between pictures

      Args:
        indexFrom (int):  The current index of the picture
        indexTo   (int):  The destination index of the picture 
    """
    state = self.pictureManager.move( \
      self.pictureManager.index(indexFrom, 0), \
      self.pictureManager.index(indexTo, 0))
    if state: self.pictureMoved.emit(indexTo)

  @pyqtSlot(int)
  def filterPictures(self, status):
    """
      A slot that handle filtering within pictures

      Args:
        status  (int):  The status that should be filtered, according to PictureState
    """
    regExp = QRegExp(status != -1 and str(status) or "")
    #TODO handle non discarded status
    self.pictureManager.setFilterRegExp(regExp)
    self.picturesFiltered.emit()

  @pyqtSlot(QVariant, QVariant)
  def newPictures(newPictures, deletedPictures):
    """
      Handle an update from the camera to manage new or deleted pictures.

      Args:
        newPictures (list<str>): A list of newly found pictures
        deletedPictures (list<str>): A list of all previously existing pictures now deleted by user
    """
    #self.pictureModel.deleteThumbnails(deletedPictures)
    #self.workspaceManager.deleteThumbnails(deletedPictures)
    print("TODO")    

  @pyqtSlot(QVariant)
  def importPictures(self, picturesFiles):
    """
      A slot that handle the picture import from a camera

      Args:
        picturesFiles (list<QUrl>): The list of pictures to be imported
    """
    self.workspaceManager.generateModel(picturesFiles)
    self.pictureModel.addFromXML(self.workspaceManager.pictureModelPath())
    self.pictureManager = self.pictureModel.instantiateManager()
    self.picturesImported.emit(self.pictureManager)


  def __init__(self): 
    super(Orchestrator, self).__init__()
    # Instantiate the app, and all attached logic modules
    self.app = QGuiApplication(sys.argv)
    self.workspaceManager = WorkspaceManager()
    self.pictureModel = PictureModel(self.RESOURCES)
    self.pictureFetcher = Pygphoto()
    #self.pictureFetcher.setActiveMode(True) # Default, watch for new files
    #self.pictureFetcher.setWatchCamera(True) 

    # Initialize and configure all modules
    # Temporary, photos will be added by signals
    self.workspaceManager.setProjectPath("Workspace/project1/")
    

    # Instantiate the view
    engine = QQmlApplicationEngine()
    engine.addImportPath(self.QML_PACKAGE)

#    # Temporary, model will be supplied by another module
#    thumbnailsPath = os.path.join(os.getcwd(), "Workspace", "project1", "thumbnails")
#    engine.rootContext().setContextProperty("thumbnailsPath", thumbnailsPath)

    engine.load(QUrl(self.MAIN_VIEW))
    self.root = engine.rootObjects()[0]

    # Link every slots
    self.connectEverything()
    
    # Let's have fun !
    self.root.show()

  def connectEverything(self):
    """
      Every connections between slots and signals are done here
    """
    self.root.sig_filterPictures.connect(self.filterPictures)
    self.root.sig_movePicture.connect(self.movePicture)
    self.root.sig_importPictures.connect(self.importPictures)
    
    self.pictureMoved.connect(self.root.slot_pictureMoved)
    self.picturesFiltered.connect(self.root.slot_picturesFiltered)

    self.picturesImported.connect(self.root.slot_picturesImported)
    #self.pictureFetcher.cameraUpdated(self.root.slot_cameraUpdated)
    #self.pictureFetcher.newPictures(self.newPictures)

if __name__ == "__main__":
  matrix = Orchestrator()
  sys.exit(matrix.app.exec_())
