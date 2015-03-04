#! /usr/bin/python3
#import interfaceReconstruction
import sys, signal, os
from OpenGL import GL
from PyQt5.QtQuick import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtQml import *
from Components.PyQt.PictureManager.pictureManager import *
from Components.PyQt.WorkspaceManager.WorkspaceManager import WorkspaceManager
from Components.PyQt.PictureFetcher.pygphoto import *

class Orchestrator(QObject):
    MAIN_VIEW = os.path.join(os.getcwd(), "MainWindow.qml")
    QML_PACKAGE = os.path.join(os.getcwd(), "Components", "QML")
    RESOURCES = os.path.join(os.getcwd(), "Resources")

    # Define all sendable signals
    # Send to inform view that picture has been moved  
    picturesMoved = pyqtSignal(QVariant, int)
    # Send to inform that pictures have been filtered
    picturesFiltered = pyqtSignal()
    # Send to inform that picture have been imported. 
    picturesImported = pyqtSignal(QVariant)

    # Define All Usable Slots
    @pyqtSlot(QVariant, int)
    def movePictures(self, indexes, startIndexTo):
        """
        A slot that handle the reorganization between pictures. If more than one 
        index are supplied, the first pictures selected will be moved at indexTo, 
        and the other will be appended

        Args:
        indexes (list<int>):  Indexes to be moved
        startIndexTo   (int):  The destination start index of all pictures
        """
        offsetDown = 0; offsetUp = 0; 
        state = True
        indexes = indexes.toVariant()
        indexes.sort()
        for indexFrom in indexes:
            indexFrom = max(0, indexFrom - offsetDown)
            indexTo = min(self.pictureManager.rowCount() - 1, startIndexTo + offsetUp)
            state = state and self.pictureManager.move( \
                self.pictureManager.index(indexFrom, 0), \
                self.pictureManager.index(indexTo, 0))
            if(indexFrom < indexTo): offsetDown += 1
            if(indexFrom > indexTo): offsetUp += 1
        if state: self.picturesMoved.emit(indexes, startIndexTo)

    @pyqtSlot(int)
    def filterPictures(self, status):
        """
        A slot that handle filtering within pictures

        Args:
        status  (int):  The status that should be filtered, according to 
        PictureState
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
            deletedPictures (list<str>): A list of all previously existing pictures 
            now deleted by user
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

    #### WORKSPACE MANAGER SLOTS

    @pyqtSlot("QString", "QString")
    def new_workspace(self,name, path):
        self.workspaceManager.new_workspace(name, path)

    @pyqtSlot("QString")
    def open_workspace(self, path):
        (directory_path,file_name) = os.path.split(path)
        self.workspaceManager.open_workspace(directory_path, file_name)

    @pyqtSlot("QString")
    def close_workspace(self, path):
        #self.workspaceManager.close_workspace(path)
        pass

    @pyqtSlot("QString")
    def change_workspace(self, path):
        self.workspaceManager.change_workspace(path)

    @pyqtSlot()
    def save_workspace(self):
        pass

    @pyqtSlot()
    def delete_workspace(self):
        pass

    @pyqtSlot()
    def new_scene(self):
        pass

    @pyqtSlot()
    def change_scene(self):
        pass

    @pyqtSlot()
    def delete_scene(self):
        pass

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

        engine.rootContext().setContextProperty("mapViewerDefaultVisible", False)

        # The list model of opened workspaces
        engine.rootContext().setContextProperty("workspacesModel",self.workspaceManager.workspaces_model)

        engine.load(QUrl(self.MAIN_VIEW))
        self.root = engine.rootObjects()[0]

        # Link every slots
        self.connectEverything()

        # Let's have fun !
        self.root.show()
        self.app.exec_()

    def connectEverything(self):
        """
        Every connections between slots and signals are done here
        """
        self.root.sig_filterPictures.connect(self.filterPictures)
        self.root.sig_movePictures.connect(self.movePictures)
        self.root.sig_importPictures.connect(self.importPictures)

        self.picturesMoved.connect(self.root.slot_picturesMoved)
        self.picturesFiltered.connect(self.root.slot_picturesFiltered)

        self.picturesImported.connect(self.root.slot_picturesImported)
        #self.pictureFetcher.cameraUpdated(self.root.slot_cameraUpdated)
        #self.pictureFetcher.newPictures(self.newPictures)

        ######## workspace manager signals
        self.root.sig_newWorkspace.connect(self.new_workspace)
        self.root.sig_openWorkspace.connect(self.open_workspace)
        self.root.sig_closeWorkspace.connect(self.close_workspace)
        self.root.sig_changeWorkspace.connect(self.change_workspace)
        self.root.sig_deleteWorkspace.connect(self.delete_workspace)
        self.root.sig_newScene.connect(self.new_scene)
        self.root.sig_changeScene.connect(self.change_scene)
        self.root.sig_deleteScene.connect(self.delete_scene)

if __name__ == "__main__":
    matrix = Orchestrator()
