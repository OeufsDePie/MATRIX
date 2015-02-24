#! /usr/bin/python3
import interfaceReconstruction
import sys,signal
from PyQt5.QtQuick import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtQml import *
from components.PyQt.PictureManager import PictureManager
from components.PyQt.WorkspaceManager import WorkspaceManager

MAIN_VIEW = './MainWindow.qml'
QML_PACKAGE = './components/QML'

# Instanciate the app, and all attached logic modules
app = QGuiApplication(sys.argv)
#iR = interfaceReconstruction.Ireconstruction('folderPly/','folderPhoto/')
workspaceManager = WorkspaceManager()
pictureManager = PictureModel()

# Initialize and configure all modules
    # Temporary, photos will be added by signals
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

# Start the app and show the view
root.show()
sys.exit(app.exec_())