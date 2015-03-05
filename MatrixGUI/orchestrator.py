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
#from Components.PyQt.ReconstructionManager.ReconstructionManager import ReconstructionManager
from orchestratorSlots import OrchestratorSlots

class Orchestrator(OrchestratorSlots):
    MAIN_VIEW = os.path.join(os.getcwd(), "MainWindow.qml")
    QML_PACKAGE = os.path.join(os.getcwd(), "Components", "QML")
    QML_PLUGIN = os.path.join(os.getcwd(),"Components", "QML", "3dRendering")
    RESOURCES = os.path.join(os.getcwd(), "Resources")
    OPENMVG_BUILD_DIR = os.path.join(os.getcwd(),"Components","PyQt","ReconstructionManager","openMVG_Build")

    def __init__(self): 
        super(Orchestrator, self).__init__()
        # Instantiate the app, and all attached logic modules
        self.app = QGuiApplication(sys.argv)
        self.workspaceManager = WorkspaceManager()
        self.pictureModel = PictureModel(self.RESOURCES)
        self.pictureFetcher = Pygphoto(watch_camera=True)
        #self.reconstructionManager = ReconstructionManager()

        # Initialize and configure all modules
        # Temporary, photos will be added by signals
        self.workspaceManager.setProjectPath("Workspace/project1/")

        # Instantiate the view
        engine = QQmlApplicationEngine()
        engine.addImportPath(self.QML_PACKAGE)
        engine.addImportPath(self.QML_PLUGIN)

        # Initialization of some parameters in the view
        engine.rootContext().setContextProperty("mapViewerDefaultVisible", False)
        engine.rootContext().setContextProperty("cameraDefaultConnected", self.pictureFetcher.check_camera_connected())
        engine.rootContext().setContextProperty("cameraDefaultName", self.pictureFetcher.query_camera_name())

        # The list model of opened workspaces and scenes
        engine.rootContext().setContextProperty("workspacesModel",self.workspaceManager.workspaces_model)
        engine.rootContext().setContextProperty("scenesModel",self.workspaceManager.scenes_model)

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
        ######## Picture Widget Signals/Orders
        self.root.sig_filterPictures.connect(self.filterPictures)
        self.root.sig_movePictures.connect(self.movePictures)
        self.root.sig_importPictures.connect(self.importPictures)
        self.root.sig_discardPictures.connect(self.discardPictures)
        self.root.sig_deletePictures.connect(self.deletePictures)

        ######## Picture Widget Callbacks/Infos
        self.picturesMoved.connect(self.root.slot_picturesMoved)
        self.picturesFiltered.connect(self.root.slot_picturesFiltered)
        self.picturesImported.connect(self.root.slot_picturesImported)
        self.picturesDiscarded.connect(self.root.slot_picturesDiscarded)
        self.picturesDeleted.connect(self.root.slot_picturesDeleted)

        ######## Picture Fetcher Signals
        self.pictureFetcher.onCameraConnection.connect(self.cameraConnection)
        self.onCameraConnection.connect(self.root.slot_cameraConnection)
        
        ######## Reconstruction Signals
        # self.root.sig_launchReconstruction.connect(self.launchReconstruction)  

        ######## workspace manager signals
        self.root.sig_newWorkspace.connect(self.new_workspace)
        self.root.sig_openWorkspace.connect(self.open_workspace)
        self.root.sig_closeWorkspace.connect(self.close_workspace)
        self.root.sig_changeWorkspace.connect(self.change_workspace)
        self.root.sig_saveWorkspace.connect(self.save_workspace)
        self.root.sig_deleteWorkspace.connect(self.delete_workspace)
        self.root.sig_newScene.connect(self.new_scene)
        self.root.sig_changeScene.connect(self.change_scene)
        self.root.sig_deleteScene.connect(self.delete_scene)

if __name__ == "__main__":
    matrix = Orchestrator()
