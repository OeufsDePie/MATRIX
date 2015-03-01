import QtQuick 2.0
import QtQuick.Controls 1.3 
import QtQuick.Controls.Styles 1.3
import QtQuick.Layouts 1.1

Rectangle {
  id: pictureWidget
  property variant pictures

  /* Raised each time a picture is re-ordered */
  signal movePictures(variant indexes, int indexTo)
  /* Raised when a picture is deleted/discarded */
  signal discardPicture(int index)
  /* Raised when ordering a filter */
  signal filterPictures(int status)

  width: 300
  /* First element is only a little picture viewer, as a box that contains an image  */
  Rectangle {
    id: viewerWrapper
    width: pictureWidget.width 
    height: width
    anchors.top: parent.top
    anchors.left: parent.left
    Image {
      id: viewer
      anchors.fill: parent
      anchors.centerIn: parent
      fillMode: Image.PreserveAspectCrop
      sourceSize.width: 2 * viewerWrapper.width
      clip: true
    }
  }

  /* Just a separator */
  Separator {
    id: separator1
    anchors.top: viewerWrapper.bottom
  }

  ComboBox {
    id: filters
    anchors.top: separator1.bottom
    anchors.right: parent.right
    width: pictureWidget.width / 3
    height: 25
    model: ListModel {
      id: filterModel
      ListElement { text: "All"; value: -1 }
      ListElement { text: "New"; value: 0 }
      ListElement { text: "Reconstruction"; value: 1 }
      ListElement { text: "Processed"; value: 3 }
      ListElement { text: "Discarded"; value: 2 }
    }
    /* Filter all pictures below */
    onCurrentIndexChanged: {
      filterPictures(filterModel.get(filters.currentIndex).value)
    }  
  }

  /* Just a separator */
  Separator {
    id: separator2
    anchors.top: filters.bottom
  }

  /* Then is the complete list of pictures, only names are displayed */
  Item {
    anchors.top: separator2.bottom
    anchors.bottom: parent.bottom
    width: parent.width

    /* ScrollView will easily handle the data overflow */
    ScrollView {
      id: scrollView 

      anchors.fill: parent
      /* Little hack because it seems that  ****** people like putting default padding */
      Component.onCompleted: {
        __style.padding.top = 0
        __style.padding.bottom = 0
        __style.padding.left = 0
        __style.padding.right = 0
      }
      ListView {
        id: listView
        boundsBehavior: Flickable.StopAtBounds
        currentIndex: 0
        model: pictures
        delegate: pictureDelegate

        Item {
          id: selectedPictures
          property variant model: ListModel {}
        }
      }
    }
  }

  /* Define delegate for the view */
  Rectangle {
    id: dragIndicator
    width: pictureWidget.width
    anchors.top: separator2.bottom
    height: 2
    color: "#76d2fe"
    visible: false
  }

  Component {
    id: pictureDelegate
    Rectangle {
      id: pictureWrapper

      property bool isFocused: false
      property bool isSelected: _isSelected(name)
      property bool isHovered: false
      property string imagePath: path

      height: pictureName.height
      width: pictureWidget.width
      color: isSelected ? "#1db7ff" : "transparent";
      border {width: isHovered ? 2 : 0; color: "#76d2fe"}

      /* Initialize the viewer with the first loaded element of the model */
      Component.onCompleted: {
        if(index == listView.currentIndex) {
          viewer.source = path
          isFocused = true
          /* If Selected and reCompleted, it's probably because the element have been moved */
          if(isSelected) {
            selectedPictures.model.setProperty(name, "index", index);
            console.log(selectedPictures.model);
          }
        }
      }
      RowLayout {
        /* Icon that represent the image status */
        anchors.left: parent.left
        anchors.leftMargin: spacing * (isFocused ? 2 : 1)
        spacing: 10
        
        Image {
          anchors.verticalCenter: parent.verticalCenter
          height: width
          source: icon
          sourceSize.height: width
          sourceSize.width: width
          width: pictureName.height * 0.75
        }
        Text {
          id: pictureName
          anchors.top: parent.top
          text: name
          color: "#000000"
        }
      }
      /* An Indicator for hovering */
      Rectangle {
        width: isHovered ? 8 : 0
        height: pictureWrapper.height
        anchors.left: pictureWrapper.left
        color: "#76d2fe"
      }

      /* Handle mouseClick in order to update the pictureViewer. Also
       in charge of reordering element via drag'n'drop */
       MouseArea {
          id: dragArea

          /* Properties use to handle the drag and drop */
          property int positionStarted
          property int positionEnded
          property int indexMoved: Math.floor((positionEnded - positionStarted)/pictureWrapper.height)
          property int newIndex: Math.min(Math.max(0, index + indexMoved), listView.model.count() - 1)

          acceptedButtons: Qt.LeftButton | Qt.RightButton
          anchors.fill: parent
          drag.axis: Drag.YAxis
          drag.minimumY: 0
          drag.maximumY: listView.model.count() * pictureWrapper.height
          drag.target: null
          hoverEnabled: true

          onEntered: { isHovered = true }
          onExited: { isHovered = false }
          onPressed: {
            if(mouse.button == Qt.LeftButton) {
              positionStarted = pictureWrapper.y
              /* Sounds glitchy, but we also initialize the positionEnded to handle simpleClick for which,
              onPositionChanged never get called */
              positionEnded = positionStarted
              dragArea.drag.target = pictureWrapper
            }
          }
          onPositionChanged: {
            if(dragArea.drag.target != null) {
              pictureWrapper.opacity = 0.3
              positionEnded = pictureWrapper.y
              dragIndicator.visible = true
              dragIndicator.anchors.topMargin = newIndex * pictureWrapper.height
              if(indexMoved > 0) dragIndicator.anchors.topMargin += pictureWrapper.height
            }
          }
          /* On release, click or move element, depending of the executed action */
          onReleased: {
            if(mouse.button == Qt.RightButton) {
              _unselect(name);
            } else {
              pictureWrapper.opacity = 1
              dragArea.drag.target = null
              pictureWrapper.y = positionStarted
              dragIndicator.visible = false
              /* indexMoved == 0 means that the item wasn't drag, so it's considered as a click */
              if (indexMoved != 0) {
                /* Send the corresponding signal */
                var indexes = _selectedIndexes();
                indexes = indexes.length == 0 ? [index] : indexes;
                movePictures(indexes, newIndex);
              } else {
                /* Only a click, so select the element in the viewer */
                viewer.source = path
                if(mouse.modifiers & Qt.ControlModifier) {
                  if(!_isSelected(name)) {
                    selectedPictures.model.append({"idSelected": name, "index": index});
                  }
                } else if(mouse.modifiers & Qt.ShiftModifier) {

                } else {
                  listView.currentItem.isFocused = false
                  listView.currentIndex = index
                  isFocused = true
                }
              }
            }
          }
        }
      }
    }

    function _iterateOnSelected(id, callback) {
      for(var i = 0; i < selectedPictures.model.count; i++) {
        if(selectedPictures.model.get(i).idSelected == id) {
          return callback(i);
        }
      }
      return false;
    }

    function _unselect(id) {
      _iterateOnSelected(id, function(i){
        selectedPictures.model.remove(i);
      });
    }

    function _isSelected(id) {
      return _iterateOnSelected(id, function(i){ return true; });
    }

    function _selectedIndexes() {
      var indexes = [];
      for(var i = 0; i < selectedPictures.model.count; i++)
        indexes.push(selectedPictures.model.get(i).index);
      return indexes;
    }


    function refreshModel() {
      listView.model = [];
      listView.model = pictures;
    }

    function picturesMoved(indexFrom, indexTo){
      refreshModel();
      listView.currentIndex = indexTo;
      listView.currentItem.isFocused = true;
      viewer.source = listView.currentItem.imagePath
      selectedPictures.model.clear();
    }

    function picturesFiltered(){
      refreshModel();
      /* Repaint the viewer if needed */
      if(listView.currentItem){ 
        listView.currentItem.Component.completed();
      } else {
        viewer.source = "";
      }
    }
}
