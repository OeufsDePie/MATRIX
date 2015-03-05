from PyQt5.QtCore import *

class OrchestratorSlots(QObject):
  # Define all sendable signals
  # Send to inform view that picture has been moved  
  picturesMoved = pyqtSignal(QVariant, int)
  # Send to inform that pictures have been filtered
  picturesFiltered = pyqtSignal()
  # Send to inform that picture have been imported. 
  picturesImported = pyqtSignal(QVariant)
  # Send to inform that pictures have been discarded
  picturesDiscarded = pyqtSignal(QVariant)
  # Send to inform that pictures have been deleted
  picturesDeleted = pyqtSignal(QVariant)

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
          status  (int):  The status that should be filtered, according to PictureState
      """
      regExp = QRegExp(status != -1 and str(status) or "")
      #TODO handle non discarded status
      self.pictureManager.setFilterRegExp(regExp)
      self.picturesFiltered.emit()

  @pyqtSlot(QVariant)
  def discardPictures(self, indexes):
      """
      A slot that handle picture discarding

      Args: 
          indexes (list<QVariant>): Indexes of pictures to discard
      """
      state = self.pictureManager.discardAll(\
          [ self.pictureManager.index(i, 0) for i in indexes.toVariant() ])
      if(state): self.picturesDiscarded.emit(indexes)

  @pyqtSlot(QVariant)
  def deletePictures(self, indexes):
      """
      A slot that handle picture deleting

      Args: 
          indexes (list<QVariant>): Indexes of pictures to delete
      """
      print(indexes.toVariant())
      state = self.pictureManager.deleteAll(\
          [ self.pictureManager.index(i, 0) for i in indexes.toVariant() ])
      if(state): self.picturesDeleted.emit(indexes)


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
      self.workspaceManager.close_workspace(path)

  @pyqtSlot("QString")
  def change_workspace(self, path):
      self.workspaceManager.change_workspace(path)

  @pyqtSlot("QString", "QString")
  def save_workspace(self, name, path):
      self.workspaceManager.save_workspace(path, name)

  @pyqtSlot("QString")
  def delete_workspace(self, path):
      self.workspaceManager.delete_workspace(path)

  @pyqtSlot("QString")
  def new_scene(self, name):
      self.workspaceManager.new_scene(name)

  @pyqtSlot("QString")
  def change_scene(self, path):
      self.workspaceManager.change_scene(path)

  @pyqtSlot("QString")
  def delete_scene(self, path):
      self.workspaceManager.delete_scene(path)