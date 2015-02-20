import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtQuick import *

# Instanciation de l'application
app = QGuiApplication(sys.argv)

# Recuperation de la vue qml
# This may be changed in the future. Using ApplicationWindow in QML is incompatible with QQuickView. 
# Better Using the QQMLApplicationEngine from PyQt5.QtQml
view = QQuickView()
view.setSource(QUrl('testSignal.qml'))
view.setResizeMode(QQuickView.SizeRootObjectToView)

# Creation d'un signal
class Signal(QObject):
    myPythonSignal = pyqtSignal(str) 

    # Creation de slots
    def myPythonSlot(self):
    	print("My Python Slot Is Called")

    def triggerMySignal(self):
    	self.myPythonSignal.emit("This message came from Python <3")

sigObj = Signal()

# Connect everything
sigObj.myPythonSignal.connect(view.rootObject().myQmlSlot)
view.rootObject().myQmlSignal.connect(sigObj.myPythonSlot)
view.rootObject().triggerMySignal.connect(sigObj.triggerMySignal)

# Start The app
view.setGeometry(100,100,640,480)
view.show()

sys.exit(app.exec_())



