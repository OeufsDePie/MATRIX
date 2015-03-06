from PyQt5.QtCore import *
from Savable import Savable # Need __init__
import xml.etree.ElementTree as ET
import os, exiftool

class PictureState():
    """
    An Enumeration to handle all different state in which a picture may be
    """
    NEW = 0 # The picture is newly added to the set of pictures
    RECONSTRUCTION = 1 # A newly added picture used for a reconstruction
    REJECTED = 2 # A picture rejected after a reconstruction, will not be used for next reconstruction
    PROCESSED = 3 # A processed pictures, used for a reconstruction and not rejected
    THUMBNAIL = 4 # Only a thumbnail corresponding to an existing picture to be imported
    THUMBNAIL_DISCARDED = 5 # Discard a thumbnail in order to suppress the thumbnail on real import
    DISCARDED = 6 # Discarded pictures will not be used for the reconstruction
  
class Picture(object):
    """
    A container used to store all data about a particular picture. It reflects an xml
    structure and is used to manipulate photos as dataModel along the use of the application
    """
    def __init__(self, resourcesPath, path, latitude, longitude, date = None, \
        status = PictureState.NEW):
        """
          Initialize a picture. 
          
          Args: 
            path    (str): path to the picture file
            date    (str): the date the photo has been taken 
            status  (str): the status of the picture, see PictureState upon
        """
        self.path, self.status, self._resourcesPath = path, status, resourcesPath
        self.latitude, self.longitude = latitude, longitude
        self.date = date
        self.name = os.path.basename(self.path)

    @pyqtProperty(str)
    def icon(self):
        """
        Retrieve the icon corresponding to the picture's status

        Returns: 
        str: The path to the icon file. 
        """
        return os.path.join(self._resourcesPath, "Icons", str(self.status) + ".png")

    def serialize(self):
        """ Serialize a Picture object.
        """
        serial = dict()
        serial['path'] = self.path
        serial['latitude'] = self.latitude
        serial['longitude'] = self.longitude
        serial['status'] = self.status
        serial['date'] = self.date
        return serial



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

    @pyqtSlot(int, result=str)
    def getName(self, index):
        return self.sourceModel().data(self.sourceModel().index(index), PictureModel.NAME_ROLE)

    @pyqtSlot(result=QVariant)
    def computeCenter(self):
        """
        Compute the coordinates of the center associated to all pictures

        Returns:
            list<float>: The coordinates, latitude then longitude
        """
        extract = lambda coord: [ float(getattr(d, coord)) for d in self.sourceModel()._data if getattr(d, coord) != "0.0" ]
        latitudes = extract('latitude'); longitudes = extract('longitude')
        coords = {'latitude': 0, 'longitude': 0}
        if(len(latitudes) > 0 and len(longitudes) > 0):
            average = lambda list: sum(list) / len(list)
            coords['latitude'] = average(latitudes)
            coords['longitude'] = average(longitudes)
        #Else, throw an error to inform the user ?
        return coords

    def _iterateOverRows(self, rows):
        """
        Iterate over rows in the model that may change during the iteration

        Args:
            rows (list<QModelIndex>): The related rows in the proxy model
        """
        processed = [] # Holds all rows already been processed
        previousSize = self.count()
        for row in rows:
            if row.isValid(): 
                processed.append(row.row())
                if previousSize != self.count():
                    previouslyProcessed = [ p for p in processed if p < row.row() ]
                    row = self.index(row.row() - len(previouslyProcessed), 0)
                    previousSize = self.count()
                yield row

    def discardAll(self, rows):
        """
        Change the status of pictures to DISCARDED or THUMBNAIL_DISCARDED

        Args:
            rows (list<QModelIndex>): The related rows in the proxy model
        """
        state = True
        for row in self._iterateOverRows(rows):
            currentStatus = self.data(row, PictureModel.STATUS_ROLE)
            newStatus = currentStatus == PictureState.THUMBNAIL and PictureState.THUMBNAIL_DISCARDED\
                or PictureState.DISCARDED
            state = state and self.setData(row, newStatus, PictureModel.STATUS_ROLE)
        return state

    def deleteAll(self, rows):
        """
        Remove pictures from the model

        Args:
            rows (list<QModelIndex>): The related rows in the proxy model
        """
        state = True
        for row in self._iterateOverRows(rows):
            state = state and self.removeRow(row.row())
        return state

    def move(self, initRow, finalRow):
        """
          Move a row from an index to another. Exactly, put initRow after 
          finalRow if moving up to down, and before finalRow if moving down to up
          
          Args:
            initRow   (QModelIndex): The starting index
            finalRow  (QModelIndex): The final index
        """
        # Ensure the index is correct
        if not initRow.isValid() or not finalRow.isValid():
            return False

        outOfBounds = lambda index, sup: index < 0 or index >= sup
        if outOfBounds(initRow.row(), self.rowCount()) or \
            outOfBounds(finalRow.row(), self.rowCount()): return False

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

class MetaPictureModel(pyqtWrapperType, Savable):
    pass

class PictureModel(QAbstractListModel, metaclass=MetaPictureModel):
    """
    Represent and handle a list of pictures as a ListModel. Directly implements 
    QAbstractListModel.

    Attributes:
      PATH_ROLE     (int): Role that handle the picture's path name of an item
      NAME_ROLE     (int): Role that handle the picture's name of an item
      DATE_ROLE     (int): Role that handle the picture's date of creation 
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
    LATITUDE_ROLE = Qt.UserRole + 6
    LONGITUDE_ROLE = Qt.UserRole + 7
    ITEM_ROLE = Qt.UserRole + 50
    _roles = {
        PATH_ROLE: "path", 
        NAME_ROLE: "name", 
        DATE_ROLE: "date", 
        STATUS_ROLE: "status", 
        ICON_ROLE: "icon",
        ITEM_ROLE: "item",
        LATITUDE_ROLE: "latitude",
        LONGITUDE_ROLE: "longitude"
    }

    def __init__(self, resourcesPath, listPictures = [], parent = None):
        """ 
          Initialize a picture model
          
          Args:
            resourcesPath (str): Path to the resources folder of the application. 
            listPictures  (str): The list of pictures to use, could be empty and 
                specified later
            parent        (str): Parent Element; May remains None in our case
        """
        super(PictureModel, self).__init__(parent)
        self._resourcesPath = resourcesPath
        self._data = listPictures

    def instantiateManager(self):
        """
          Create an instance of this model manager. The manager add an indirection 
          that allow, for instance, filtering. 

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
            index -- The index where the picture should be inserted. If None, 
            the picture will be appended at the end.
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

    def removeRows(self, row, count, parent = QModelIndex()):
        """
        Remove contiguous pictures from the model

        Args
            row     (int)           : The first picture's index
            count   (int)           : Number of picture to remove
            parent  (QModelIndex)   : The parent row
        """
        # Ensure the index is correct
        if len(self._data) <= 0:
            return False

        if row < 0 or count < 1 or row + count - 1 >= self.rowCount():
            return False

        self.beginRemoveRows(QModelIndex(), row, row + count - 1)
        #Deleting row starting by the latest index
        for i in range(0, count):
            del self._data[row + count - i - 1]
        self.endRemoveRows()
        return True

    def removeRow(self, row, parent = QModelIndex()):
        """
          Remove a picture from the model

          row -- The picture"s index
        """
        self.removeRows(row, 1, parent)

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
    
    def populate(self, picturesFiles, status = PictureState.NEW):
        """
        Populate the model, i.e. add instance of pictures element. Element are added
        with the status "NEW"

        Args:
            picturesFiles   (list<str>) : List of path to the different pictures
            status          (int) : The initial status to assign to the item
        """
        print(status)
        with exiftool.ExifTool() as exifparser:
            for url in picturesFiles:
                # Get EXIF data
                exifData = exifparser.get_tags(\
                    ['EXIF:GPSLatitude', 'EXIF:GPSLongitude'], url)
                if not ('EXIF:GPSLatitude' in exifData):
                    #May raise an error if no GPS data ?
                    exifData['EXIF:GPSLatitude'] = "0.0"
                    exifData['EXIF:GPSLongitude'] = "0.0"

                self.add(Picture(self._resourcesPath, url, \
                    str(exifData['EXIF:GPSLatitude']), str(exifData['EXIF:GPSLongitude']), \
                        status = status))

    def serialize(self):
        """ Serialize a pictureModel object.
        """
        serial = dict()
        serial['pictures'] = []
        for picture in self._data:
            serial['pictures'].append(picture.serialize())
        serial['resourcesPath'] = self._resourcesPath
        return serial

    @staticmethod
    def deserialize(serial):
        """ Recreate a pictureModel object from its serialization.

        Args:
            serial (dict()): The serialized version of a pictureModel object.
        """
        pictureModel = PictureModel(serial['resourcesPath'])
        for picture in serial['pictures']:
            pictureModel.add(Picture(serial['resourcesPath'], picture['path'],\
                picture['latitude'], picture['longitude'], picture['date'], picture['status']))

        return pictureModel

    def save(self, base_path, file_name):
        """ Save the object in the file system.
        """
        Savable.save(self, base_path, file_name)

    @classmethod
    def load(cls, base_path, file_name, object_class=None):
        """ Recreate a pictureModel object from a file.

        Args:
            base_path (str): The path of the directory containing the file.
            file_name (str): The name of the file to load.
            object_class (class): The class of the object to recreate.
        """
        if object_class == None:
            object_class = cls
        return Savable.load(base_path, file_name, object_class)