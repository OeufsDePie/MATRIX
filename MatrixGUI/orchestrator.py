#! /usr/bin/python3
#import interfaceReconstruction
import sys, signal, os
#from OpenGL import GL
from PyQt5.QtQuick import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtQml import *
from components.PyQt.PictureManager.PictureManager import *
from components.PyQt.WorkspaceManager.WorkspaceManager import *

class Orchestrator(QObject):
  MAIN_VIEW = os.path.join(os.getcwd(), "MainWindow.qml")
  QML_PACKAGE = os.path.join(os.getcwd(), "components", "QML")
  RESOURCES = os.path.join(os.getcwd(), "Resources")

  # Define all sendable signals
  pictureMoved = pyqtSignal(int)
  picturesFiltered = pyqtSignal()

  # Define All Usable Slots
  @pyqtSlot(int, int)
  def movePicture(self, indexFrom, indexTo):
    '''
      A slot that handle the reorganization between pictures
    '''
    state = self.pictureManager.move( \
      self.pictureManager.index(indexFrom, 0), \
      self.pictureManager.index(indexTo, 0))
    if state: self.pictureMoved.emit(indexTo)

  @pyqtSlot(int)
  def filterPictures(self, status):
    '''
      A slot that handle filtering within pictures
    '''
    regExp = QRegExp(status != -1 and str(status) or "")
    self.pictureManager.setFilterRegExp(regExp)
    self.picturesFiltered.emit()

  def __init__(self): 
    super(Orchestrator, self).__init__()
    # Instantiate the app, and all attached logic modules
    app = QGuiApplication(sys.argv)
    #iR = interfaceReconstruction.Ireconstruction('folderPly/','folderPhoto/')
    self.workspaceManager = WorkspaceManager()
    pictureModel = PictureModel(self.RESOURCES)

    # Initialize and configure all modules
    # Temporary, photos will be added by signals
    self.workspaceManager.setProjectPath('Workspace/testPics/')
    pictureModel.addFromXML(self.workspaceManager.pictureModelPath())

    # Instantiate the view
    engine = QQmlApplicationEngine()
    engine.addImportPath(self.QML_PACKAGE)

    # Temporary, model will be supplied by another module
    self.pictureManager = pictureModel.instantiateManager()
    engine.rootContext().setContextProperty('pictureModel', self.pictureManager)

    engine.load(QUrl(self.MAIN_VIEW))
    self.root = engine.rootObjects()[0]

    self.connectEverything()

    self.root.show()
    sys.exit(app.exec_())

  def connectEverything(self):
    # Connect signals to slots
    # iR.connectSignalPly(root.slot_addLog)
    # root.sig_launchReconstruction.connect(iR.startReconstruction)
    self.root.sig_movePicture.connect(self.movePicture)
    self.root.sig_filterPictures.connect(self.filterPictures)
    self.pictureMoved.connect(self.root.slot_pictureMoved)
    self.picturesFiltered.connect(self.root.slot_picturesFiltered)

if __name__ == '__main__':
  matrix = Orchestrator()
