from PyQt5.Qtcore import QAbstractListModel, Qt, QModelIndex, pyqtSlot, QObject
from enum import Enum
import xml.etree.ElementTree as ET

class PictureState(Enum):
  '''
    An Enumeration to handle all different state in which a picture may be
  '''
  NEW = 0 # The picture is newly added to the set of pictures
  RECONSTRUCTION = 1 # A newly added picture used for a reconstruction
  REJECTED = 2 # A picture rejected by user or after a reconstruction (may be splitted)
  PROCESSED = 3 # A processed pictures, used for a reconstruction and not rejected
  
class Picture(object):
  '''
    A container used to store all data about a particular picture. It reflects an xml
    structure and is used to manipulate photos as dataModel along the use of the application
  '''

  def __init__(self, path, date, state = PictureState.NEW):
    '''
      Initialize a picture. 
      
      path  -- path to the picture file (!TODO specified relative path) 
      date  -- the date the photo has been taken 
      state -- the state of the picture, see PictureState upon
    '''
    self.path, self.date, self.state = path, date, state
    self.name = os.path.basename(self.path)

class PictureModel(QAbstractListModel):
  '''
    Represent and handle a list of pictures as a ListModel. Directly implements QAbstractListModel.
  '''
  #Roles of our model, used in QML side to retrieve data from our model
  PATH_ROLE = Qt.UserRole + 1
  NAME_ROLE = Qt.UserRole + 2
  DATE_ROLE = Qt.UserRole + 3
  STATE_ROLE = Qt.UserRole + 4
  _roles = {PATH_ROLE: 'path', NAME_ROLE: 'name', DATE_ROLE: 'date', STATE_ROLE: 'state'}

  def __init__(self, listPictures = [], parent = None)
    ''' 
      Initialize a picture model
      
      listPictures -- The list of pictures to use, could be empty and specified later
      parent -- Parent Element; May remains None in our case
    '''
    super(PictureModel, self).__init__(parent)
    self._data = listPictures # Store as an attribute the pictures for future purpose

  def data(self, index, role = PictureModel.NAME_ROLE):
    '''
      Retrieve a piece of information from an item (a picture) of the model

      index -- The index of the element
      role -- The role of the element we are interested in
    '''
    # Ensure the index
    if not index.isValid():
      return None
    elif index.row() > len(self._data):
      return None
  
    # Ensure the role
    if not role in PictureModel._roles:
      return None

    # Index and role are correct, retrieve the picture and send back the requested information
    picture = self._data[index.row()]
    return getattr(picture, PictureModel._roles[role])
  
  def roleNames(self):
    '''
      An accessor to roles names
    '''
    return self._roles

  def add(self, picture, index = None):
    '''
      Add a picture to the model

      picture -- The picture to add
      index -- The index where the picture should be inserted. If None, the picture will be
      appended at the end.
    '''
    # Ensure Index
    if not index.isValid():
      return False
    # Append at the end
    if index == None:
      self.beginInsertRows(QModelIndex(), len(self._data), len(self._data)):
      self._data.append(picture)
      self.endInsertRows()
    # Insert in the list
    else:
      row = index.row()
      if row > len(self._data):
        return False
      else
        self.beginInsertRows(QModelIndex(), row, row)
        self._data.insert(row, picture)
        self.endInsertRows()
    return True

  @pyqtSlot(QModelIndex)
  def remove(self, index):
    '''
      Remove a picture from the model

      index -- The picture's index (mdr lol)
    '''
    # Ensure the index is correct
    if len(self._data) <= 0:
      return False

    if not index.isValid():
      return False
  
    # Annihilate the item
    row = index.row()
    self.beginRemoveRows(QModelIndex(), row, row)
    del self._data[row]
    self.endRemoveRows()
    return True

  @pyqtSlot(QModelIndex, QModelIndex)
  def move(self, initRow, finalRow) 
    '''
      Move a row from an index to another.
      
      initRow -- The starting index
      finalRow -- The final index
    '''
    # Ensure index
    if not initRow.isValid() or not finalRow.isValid()
      return False

    outOfBounds = lambda index, sup: index < 0 || index >= sup
    if outOfBounds(initRow.row(), self.rowCount()) || outOfBounds(finalRow(), self.rowCount()):
      return False

    # Move picture
    picture = self._data[initRow]
    status = self.remove(initRow)
    status = status and self.add(picture, finalRow)
    return status

  def rowCount(self, parent = QModelIndex()):
    '''
      Return the number of element within that model
    '''
    return len(self._data)
  
  @pyqtProperty(int)
  def size(self):
    '''
      An alias to be used in QML as a property. We can't use the rowCount method
      as it should remain available inside the class.
    '''
    return self.rowCount()

  def setData(self, index, value, role):
    '''
      Set a particular value in the data model using his role.
 
      index -- The index of the related element
      value -- The new value
      role  -- The related role
    '''
    # Ensure index and role
    if not index.isValid() or index.row() > self.rowCount() or not role in PictureModel._roles:
      return False

    picture = self._data[index.row()]
    setattr(picture, PictureModel._roles[role], value)
    self.dataChanged(index, index)
    return True

  def printData(self):
    print(self._data)
    
  def addFromXML(self, xmlPath):
    '''
      Add picture from a xml model file
    
      xmlPath -- The path to the XML model file
    '''
    root = ET.parse(xmlPath).getroot()
    listPictures = []
    for child in root
      #name = child.attrib['name']
      path = child.text
      self.add(Picture(path))
      xmlPath -- The path to the xml file
