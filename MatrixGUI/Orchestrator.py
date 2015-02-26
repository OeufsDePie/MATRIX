#! /usr/bin/python3
#import interfaceReconstruction
import sys,signal
from PyQt5.QtQuick import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtQml import *
from components.PyQt.PictureManager.PictureManager import *
from components.PyQt.WorkspaceManager.WorkspaceManager import *

MAIN_VIEW = './MainWindow.qml'
QML_PACKAGE = './components/QML'

# Instanciate the app, and all attached logic modules
app = QGuiApplication(sys.argv)
#iR = interfaceReconstruction.Ireconstruction('folderPly/','folderPhoto/')
workspaceManager = WorkspaceManager()
pictureManager = PictureModel()

# Initialize and configure all modules
# Temporary, photos will be added by signals
workspaceManager.setProjectPath('Workspace/project1/')
pictureManager.addFromXML(workspaceManager.pictureModelPath())

# Instanciate the view
engine = QQmlApplicationEngine()
engine.addImportPath(QML_PACKAGE)

# Temporary, model will be supplied by another module
engine.rootContext().setContextProperty('pictures', pictureManager)

engine.load(QUrl(MAIN_VIEW))
root = engine.rootObjects()[0]
#Watched folder
# print('Ireconstruction is watching those folders :')
# iR.printDirWatched()

# Connect signals to slots
# iR.connectSignalPly(root.slot_addLog)
# root.sig_launchReconstruction.connect(iR.startReconstruction)
#root.pictureMoved.connect(picureManager.move)

# Start the app and show the view


#################   WORKSPACE MANAGER  #####################
#                         SLOTS
@pyqtSlot()
def new_workspace():
    workspaceManager.new_workspace("test_name","test_path")

@pyqtSlot()
def change_workspace():
    pass

@pyqtSlot()
def delete_workspace():
    pass

@pyqtSlot()
def new_scene():
    pass

@pyqtSlot()
def change_scene():
    pass

@pyqtSlot()
def save_scene():
    pass

@pyqtSlot()
def delete_scene():
    pass



#                         SIGNALS
root.sig_newWorkspace.connect(new_workspace)
root.sig_changeWorkspace.connect(change_workspace)
root.sig_deleteWorkspace.connect(delete_workspace)
root.sig_newScene.connect(new_scene)
root.sig_changeScene.connect(change_scene)
root.sig_saveScene.connect(save_scene)
root.sig_deleteScene.connect(delete_scene)
############################################################



root.show()
sys.exit(app.exec_())
