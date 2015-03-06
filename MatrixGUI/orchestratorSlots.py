import sys, signal, os
from PyQt5.QtCore import *
from Components.PyQt.PictureManager.pictureManager import PictureState

class OrchestratorSlots(QObject):
    # Define all sendable signals
    # Send to inform view that picture model has been moved  
    picturesUpdated = pyqtSignal(QVariant)
    # Send when an update about the status of the camera is available
    onCameraConnection = pyqtSignal(bool, str) 
    # Send when the workspace become available or unavailable
    workspaceAvailable = pyqtSignal(bool)
    # Send when a new reconstruction is available
    reconstructionChanged = pyqtSignal(str)

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
        self.pictureManager.sourceModel().printData()
        if state: self.picturesUpdated.emit(self.pictureManager)

    @pyqtSlot(int)
    def filterPictures(self, status):
        """
        A slot that handle filtering within pictures

        Args:
          status  (int):  The status that should be filtered, according to PictureState
        """
        regStr = str(status)
        if(status > 100):
            specials = {
                101: "",
                102: "5|6",
                103: "0|1|3"
            }
            regStr = specials[status]

        regExp = QRegExp(regStr)
        #TODO handle non discarded status
        self.pictureManager.setFilterRegExp(regExp)
        self.picturesUpdated.emit(self.pictureManager)

    @pyqtSlot(QVariant)
    def discardPictures(self, indexes):
        """
        A slot that handle picture discarding

        Args: 
          indexes (list<QVariant>): Indexes of pictures to discard
        """
        state = self.pictureManager.discardAll(\
          [ self.pictureManager.index(i, 0) for i in indexes.toVariant() ])
        if(state): self.picturesUpdated.emit(self.pictureManager)

    @pyqtSlot(QVariant)
    def renewPictures(self, indexes):
        """
        A slot that handle picture renewing, i.e, that allow rejected or
        discarded pictures to be used again

        Args: 
          indexes (list<QVariant>): Indexes of pictures to renew
        """
        state = self.pictureManager.renewAll(\
          [ self.pictureManager.index(i, 0) for i in indexes.toVariant() ])
        if(state): self.picturesUpdated.emit(self.pictureManager)

    @pyqtSlot(QVariant)
    def deletePictures(self, indexes):
        """
        A slot that handle picture deleting

        Args: 
          indexes (list<QVariant>): Indexes of pictures to delete
        """
        state = self.pictureManager.deleteAll(\
          [ self.pictureManager.index(i, 0) for i in indexes.toVariant() ])
        if(state): self.picturesUpdated.emit(self.pictureManager)


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
        newPaths = self.workspaceManager.import_pictures([ p.path() for p in picturesFiles ])
        self.pictureModel.populate(newPaths)
        self.pictureManager.setSourceModel(self.pictureModel)
        self.picturesUpdated.emit(self.pictureManager)

    #### WORKSPACE MANAGER SLOTS
    @pyqtSlot("QString", "QString")
    def new_workspace(self,name, path):
        self.workspaceManager.new_workspace(name, path)
        self.workspaceAvailable.emit(True)

    @pyqtSlot("QString")
    def open_workspace(self, path):
        (directory_path,file_name) = os.path.split(path)
        self.workspaceManager.open_workspace(directory_path, file_name)
        self.pictureModel = self.workspaceManager.getPictureModel()
        self.pictureManager.setSourceModel(self.pictureModel)
        self.picturesUpdated.emit(self.pictureManager)
        self.workspaceAvailable.emit(True)

    @pyqtSlot("QString")
    def close_workspace(self, path):
        self.workspaceManager.close_workspace(path)
        self.workspaceAvailable.emit(False)

    @pyqtSlot("QString")
    def change_workspace(self, path):
        self.workspaceManager.change_workspace(path)
        self.pictureModel = self.workspaceManager.getPictureModel()
        self.pictureManager.setSourceModel(self.pictureModel)
        self.picturesUpdated.emit(self.pictureManager)

    @pyqtSlot()
    def save_workspace(self):
        ws = self.workspaceManager.get_current_workspace()
        self.workspaceManager.save_workspace(ws.full_path())

    @pyqtSlot("QString")
    def delete_workspace(self, path):
        self.workspaceManager.delete_workspace(path)

    @pyqtSlot("QString")
    def new_scene(self, name):
        self.workspaceManager.new_scene(name)

    @pyqtSlot("QString")
    def change_scene(self, path):
        self.workspaceManager.change_scene(path)
        self.pictureModel = self.workspaceManager.getPictureModel()
        self.pictureManager = self.pictureModel.instantiateManager()
        self.picturesUpdated.emit(self.pictureManager)
        
    @pyqtSlot("QString")
    def delete_scene(self, path):
        self.workspaceManager.delete_scene(path)

    #### PICTURE FETCHER SLOTS
    @pyqtSlot(bool)
    def cameraConnection(self, isConnected):
        name = self.pictureFetcher.query_camera_name()
        self.onCameraConnection.emit(isConnected, name)

    @pyqtSlot()
    def importThumbnails(self):
        thumbnailsDir = self.workspaceManager.get_thumbnails_dir()
        thumbnailsNames = self.pictureFetcher.query_file_list()
        thumbnailsNames = self.pictureFetcher.download_files(thumbnailsNames, \
            thumbnailsDir, thumbnail=True)
        self.pictureModel.populate([ os.path.join(thumbnailsDir, n) for n in thumbnailsNames ], PictureState.THUMBNAIL)
        self.pictureManager.setSourceModel(self.pictureModel)
        self.picturesUpdated.emit(self.pictureManager)

    @pyqtSlot()
    def launchReconstruction(self):
        validFiles = self.pictureModel.validFiles()
        crapDir = self.workspaceManager.get_scene_temp_output_dir()
        inDir = self.workspaceManager.get_selected_picture_dir()
        outDir = self.workspaceManager.get_scene_output_dir()
        method = "FlawlessVictory"
        self.reconstructionManager.launchReconstruction(inDir,\
            method,\
            self.OPENMVG_BUILD_DIR,\
            crapDir,\
            outDir)
        self.reconstructionChanged.emit(os.path.join(\
            self.workspaceManager.get_current_scene().full_path(),\
            self.workspaceManager.get_current_scene().get_reconstruction_temp_dir(),\
            "FinalColorized.ply"))