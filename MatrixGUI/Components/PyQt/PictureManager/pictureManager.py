from PyQt5.QtCore import *
import xml.etree.ElementTree as ET
import os
class PictureState():
  """
    An Enumeration to handle all different state in which a picture may be
  """
  NEW = 0 # The picture is newly added to the set of pictures
  RECONSTRUCTION = 1 # A newly added picture used for a reconstruction
  REJECTED = 2 # A picture rejected by user or after a reconstruction (may be splitted)
  PROCESSED = 3 # A processed pictures, used for a reconstruction and not rejected
  THUMBNAIL = 4 # Only a thumbnail corresponding to an existing picture to be imported
  
class Picture(object):
  """
    A container used to store all data about a particular picture. It reflects an xml
    structure and is used to manipulate photos as dataModel along the use of the application
  """
  def __init__(self, resourcesPath, path, date = None, status = PictureState.NEW):
    """
      Initialize a picture. 
      
      Args: 
        path    (str): path to the picture file
        date    (str): the date the photo has been taken 
        status  (str): the status of the picture, see PictureState upon
    """
    self.path, self.date, self.status, self._resourcesPath = path, date, status, resourcesPath
    self.name = os.path.basename(self.path)

  @pyqtProperty(str)
  """
    Retrieve the icon corresponding to the picture's status

    Returns: 
      str: The path to the icon file. 
  """
  def icon(self):
    return os.path.join(self._resourcesPath, "Icons", str(self.status) + ".png")

class PictureManager(QSortFilterProxyModel):
  @pyqtSlot(result=int)
  def count(self):
    """
      An alias to be used in QML as a property. We can"t use the rowCount method
      as it should remain available inside the class.
    
      Returns: 
        int: The number of element in the model
    """
    return self.rowCount()

  def move(self, initRow, finalRow):
    """
      Move a row from an index to another. Exactly, put initRow after finalRow if moving up to down, 
      and before finalRow if moving down to up
      
      Args:
        initRow   (int): The starting index
        finalRow  (int): The final index
    """
    # Ensure the index is correct
    if not initRow.isValid() or not finalRow.isValid():
      return False

    outOfBounds = lambda index, sup: index < 0 or index >= sup
    if outOfBounds(initRow.row(), self.rowCount()) or outOfBounds(finalRow.row(), self.rowCount()):
      return False

    # Find the corresponding index in the real model
    source = self.sourceModel()
    initSourceRow = 0; finalSourceRow = 0
    for i in range(0, source.rowCount()):
      srcName = source.data(source.index(i), PictureModel.NAME_ROLE)
      filterInitName = self.data(initRow, PictureModel.NAME_ROLE)
      filterFinalName = self.data(finalRow, PictureModel.NAME_ROLE)
      initSourceRow = srcName == filterInitName and i or initSourceRow
      finalSourceRow = srcName == filterFinalName and i or finalSourceRow

    initIndex = initRow.row(); finalIndex = finalRow.row()
    if(initIndex < finalIndex):
      # Moving downside. FinalIndex should be the index of initRow new child. 
      finalIndex += 1; finalSourceRow += 1
    elif(initIndex > finalIndex):
      #Moving upside. We will insert a row before, so the index will be displaced
      initSourceRow += 1
    else:
      # Both index are equal, do nothing, there is no move
      return True

    # Move picture from source model and notify the proxy
    state = self.beginMoveRows(QModelIndex(), initIndex, initIndex, QModelIndex(), finalIndex)
    source.insertRow(finalSourceRow)
    source.setData(source.index(finalSourceRow),  \
      source.data(source.index(initSourceRow), source.ITEM_ROLE), \
      source.ITEM_ROLE)
    source.removeRow(initSourceRow)
    self.endMoveRows()

    return state

class PictureModel(QAbstractListModel):
  """
    Represent and handle a list of pictures as a ListModel. Directly implements QAbstractListModel.
  
    Attributes:
      PATH_ROLE     (int): Role that handle the picture's path name of an item
      NAME_ROLE     (int): Role that handle the picture's name of an item
      DATE_ROLE     (int): Role that handle the picture's date of creation of an item
      STATUS_ROLE   (int): Role that handle the picture's status of an item
      ICON_ROLE     (int): Role that handle the picture's icon of an item
      ITEM_ROLE     (int): Role related to the whole item / picture 
  """
  #Roles of our model, used in QML side to retrieve data from our model
  PATH_ROLE = Qt.UserRole + 1
  NAME_ROLE = Qt.UserRole + 2
  DATE_ROLE = Qt.UserRole + 3
  STATUS_ROLE = Qt.UserRole + 4
  ICON_ROLE = Qt.UserRole + 5
  ITEM_ROLE = Qt.UserRole + 50
  _roles = {
    PATH_ROLE: "path", 
    NAME_ROLE: "name", 
    DATE_ROLE: "date", 
    STATUS_ROLE: "status", 
    ICON_ROLE: "icon",
    ITEM_ROLE: "item"
  }

  def __init__(self, resourcesPath, listPictures = [], parent = None):
    """ 
      Initialize a picture model
      
      Args:
        resourcesPath (str): Path to the resources folder of the application. 
        listPictures  (str): The list of pictures to use, could be empty and specified later
        parent        (str): Parent Element; May remains None in our case
    """
    super(PictureModel, self).__init__(parent)
    self._resourcesPath = resourcesPath
    self._data = listPictures # Store as an attribute the pictures for future purpose

  def instantiateManager(self):
    """
      Create an instance of this model manager. The manager add an indirection that allow, for instance,
      filtering. 

      Returns:
        PictureManager: The picture manager corresponding to that model
    """
    manager = PictureManager()
    manager.setSourceModel(self)
    manager.setFilterRole(self.STATUS_ROLE) # Status will be used in order to filter pictures
    return manager

  def insertRow(self, row, parent = QModelIndex()):
    """
      An implementation of the parent method insertRow. It add an empty row at the given index
      See Qt Documentation for more details <3. 
      Args:
        row     (int):  The index of the future row. If superior to model size, the row will be appended. 
        parent  (QModelIndex):  The parent index, always default in our case.
      Returns:
        bool: Return True if the row have been successfully inserted.
    """
    self.beginInsertRows(QModelIndex(), row, row)
    state = self._data.insert(row, None)
    self.endInsertRows()
    return state

  def data(self, index, role = NAME_ROLE):
    """
      Retrieve a piece of information from an item (a picture) of the model

      Args: 
        index (int):  The index of the element
        role  (int):  The role of the element we are interested in
      Returns: 
        QVariant: The requested element or data related to this element. 
    """
    # Ensure the index
    if not index.isValid():
      return QVariant()
    elif index.row() > len(self._data):
      return QVariant()
  
    # Ensure the role
    if not role in PictureModel._roles:
      return QVariant()

    # Index and role are correct, retrieve the picture and send back the requested information
    picture = self._data[index.row()]
    if picture == None:
      return QVariant()

    if(role == self.ITEM_ROLE):
      return picture
    return getattr(picture, PictureModel._roles[role])
  
  def roleNames(self):
    """
      An accessor to roles names
    """
    return self._roles

  def add(self, picture, index = None):
    """
      Add a picture to the model

      picture -- The picture to add
      index -- The index where the picture should be inserted. If None, the picture will be
      appended at the end.
    """
    # Append at the end
    if index == None:
      self.beginInsertRows(QModelIndex(), len(self._data), len(self._data))
      self._data.append(picture)
      self.endInsertRows()
    # Insert in the list
    else:
      # Ensure Index
      if not index.isValid():
        return False
      row = index.row()
      if row > len(self._data):
        return False
      else:
        self.beginInsertRows(QModelIndex(), row, row)
        self._data.insert(row, picture)
        self.endInsertRows()
    return True

  def removeRow(self, row, parent = QModelIndex()):
    """
      Remove a picture from the model

      row -- The picture"s index
    """
    # Ensure the index is correct
    if len(self._data) <= 0:
      return False

    if row < 0 or row >= self.rowCount():
      return False
  
    # Annihilate the item
    self.beginRemoveRows(QModelIndex(), row, row)
    del self._data[row]
    self.endRemoveRows()
    return True

  def rowCount(self, parent = QModelIndex()):
    """
      Return the number of element within that model
    """
    return len(self._data)

  def setData(self, index, value, role):
    """
      Set a particular value in the data model using his role.
 
      index -- The index of the related element
      value -- The new value
      role  -- The related role
    """
    # Ensure index and role
    if not index.isValid() or index.row() > self.rowCount() or not role in PictureModel._roles:
      return False

    if(role == self.ITEM_ROLE):
      self._data[index.row()] = value
    else:
      picture = self._data[index.row()]
      setattr(picture, PictureModel._roles[role], value)

    self.dataChanged.emit(index, index, [role])
    return True

  def printData(self):
    for picture in self._data:
      print (picture == None and "-----" or str(picture.status) + " - " + picture.name)
    
  def addFromXML(self, xmlPath):
    """
      Add picture from a xml model file
    
      xmlPath -- The path to the XML model file
    """
    root = ET.parse(xmlPath).getroot()     
    listPictures = []
    for child in root:
      #name = child.attrib["name"]
      path = child.text
      status = child.attrib["status"]
      self.add(Picture(self._resourcesPath, path, status = status))
