import QtQuick 2.0
import QtQuick.Controls 1.3 
import QtQuick.Controls.Styles 1.3
import QtQuick.Layouts 1.1

import "Utils.js" as Utils

Rectangle {
  id: pictureWidget
  property variant pictures

  /* Make it easier to configure */
  property string borderColor: "#76d2fe"
  property string selectionColor: "#1db7ff"
  property string textColor: "#000000"

  signal discardPicture(int index) /* Raised when a picture is deleted/discarded */
  signal filterPictures(int status) /* Raised when ordering a filter */
  signal movePictures(variant indexes, int indexTo) /* Raised each time a picture is re-ordered */
  signal focusOnPicture(real latitude, real longitude) /* Raised when clicking on a picture */

  /* First element is only a little picture viewer, as a box that contains an image  */
  Viewer {
    id: viewerWrapper

    anchors {top: parent.top; left: parent.left}
    height: width
    width: pictureWidget.width 
  }

  /* Just a separator */
  Separator { id: separator1; anchors.top: viewerWrapper.bottom }

  /* Filtering button, to manage pictures visualisation easily */
  FilterButton {
    id: filterButton

    anchors {top: separator1.bottom; right: parent.right }
    height: 25
    width: pictureWidget.width / 3

    /* Filter all pictures below by triggering a signal */
    onCurrentIndexChanged: {
      filterPictures(filterButton.model.get(filterButton.currentIndex).value);
    }  
  }

  /* Just another separator */
  Separator { id: separator2; anchors.top: filterButton.bottom }

  Item {
    id: selectedPictures
    /* This little object will be used to manage selections of pictures */
    property variant model: ListModel {}
  }

  /* Then is the complete list of pictures, only names are displayed */
  Item {
    anchors {top: separator2.bottom; bottom: parent.bottom }
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
        delegate: pictureDelegate
        model: pictures
      }
    }
  }

  Component {
    id: pictureDelegate
    Rectangle {
      id: pictureWrapper

      property bool isFocused: false // Focused means that the element is the one we are seeing
      property bool isSelected: Utils.isSelected(name)
      property bool isHovered: false // Hovered means that the cursor is under this element

      property string imagePath: path // Making the image path available from the outside

      border { color: borderColor; width: isHovered ? 2 : 0 }
      color: isSelected ? selectionColor : "transparent";
      height: pictureName.height
      width: pictureWidget.width

      /* Properly, the graphical part that shows data about the picture */
      RowLayout {
        anchors { left: parent.left; leftMargin: spacing * (isFocused ? 2 : 1) }
        spacing: 10
        
        Image {
          /* Icon that represent the image status */
          anchors.verticalCenter: parent.verticalCenter
          height: width
          source: icon
          sourceSize { height: width; width: width }
          width: pictureName.height * 0.75
        }
        Text {
          /* Little text to display the name of the picture */
          id: pictureName

          anchors.top: parent.top
          color: textColor
          text: name
        }
      }

      /* An Indicator for hovering */
      Rectangle {
        anchors.left: pictureWrapper.left
        color: borderColor
        height: pictureWrapper.height
        width: isHovered ? 8 : 0
      }

      /* Now, let's have some fun ... The mouse area element handle the interaction between the user
      * and the model such as, re-ordering pictures or selecting a picture or several. */
      MouseArea {
        id: dragArea

        /* Properties use to handle the drag and drop */
        property int positionStarted  // At which position (y value, relative to parent) did we start ?
        property int positionEnded    // At which position (y value, relative to parent) did we end ?
        /* Compute, during a drag, the number of pictures we jumped */
        property int indexMoved: Math.floor((positionEnded - positionStarted)/pictureWrapper.height)
        /* Compute, during a drag, the theorically new index */
        property int newIndex: Math.min(Math.max(0, index + indexMoved), listView.model.count() - 1)
        //acceptedButtons: Qt.LeftButton | Qt.RightButton

        anchors.fill: parent
        drag.axis: Drag.YAxis
        drag.minimumY: 0
        drag.maximumY: listView.model.count() * pictureWrapper.height
        drag.target: null
        hoverEnabled: true //Allow onEntered and onExited to react at Hovering, not only clicking

        /* Use properties assignment to be more flexible. Hovering is only use to display visual 
        indicators */
        onEntered:  { isHovered = true }
        onExited:   { isHovered = false }

        onPressed: {
          /* On a click, be sure to keep in mind the position of the element currently clicked.
          Sounds glitchy, but we also initialize the positionEnded to handle simpleClick for which,
          onPositionChanged never get called */
          positionStarted = pictureWrapper.y
          positionEnded = positionStarted
          dragArea.drag.target = pictureWrapper
        }
        onPositionChanged: {
          if(dragArea.drag.target != null) {
            /* Update the position and display a little indicator during a drag */
            pictureWrapper.opacity = 0.3
            positionEnded = pictureWrapper.y
            dragIndicator.visible = true
            dragIndicator.anchors.topMargin = newIndex * pictureWrapper.height
            if(indexMoved > 0) dragIndicator.anchors.topMargin += pictureWrapper.height
          }
        }
        onReleased: {
          /* On release, click or move element(s), depending of the executed action. But, no matter
          the action, firstly clean the view and set up again a relevant state.*/
          pictureWrapper.opacity = 1
          dragArea.drag.target = null
          pictureWrapper.y = positionStarted
          dragIndicator.visible = false

          /* indexMoved != 0 means that the item wasn't drag, so it's considered as a click */
          if (indexMoved != 0) {
            /* Retrieve all selected items to move, or if none, use the dragged item */
            var indexes = Utils.selectedIndexes();
            if(indexes.length == 0 || !Utils.isSelected(name)) { indexes = [index]; }

            /* Send a signal to ask for the move */
            movePictures(indexes, newIndex);
            return;
          } 

          /* Else, we have to handle the click on different ways */
          if(mouse.modifiers & Qt.ShiftModifier && mouse.modifiers & Qt.ControlModifier) {
            /* SHIFT + CTRL Click, the user wants to select several pictures at once.
            The philosophy of the SHIFT click is to select all pictures between the shift click, and
            the last selected picture */
            if(selectedPictures.model.count > 0) {
              /* If there is no picture selected, the process will be passed to the CTRL click*/
              var start = selectedPictures.model.get(selectedPictures.model.count - 1).index
              for(var i = 1; i <= Math.abs(start - index); i++) {
                var inSelection = start + i * (start > index ? -1 : 1);
                var inSelectionName = listView.model.getName(inSelection);

                /* Ensure that we are not gonna add an already selected pictures */
                if(!Utils.isSelected(inSelectionName)){
                  selectedPictures.model.append({"idSelected": inSelectionName, "index": inSelection});
                }
              }
              return;
            }
          }

          if(mouse.modifiers & Qt.ControlModifier) {
            /* On a CTRL click, select or unselect a picture */
            Utils.togglePictureSelection(name, index);
            return;
          } 

          /* Only a simple click, so select the element in the viewer */
          viewerWrapper.viewer.source = path;
          listView.currentItem.isFocused = false;
          listView.currentIndex = index;
          focusOnPicture(latitude, longitude);
          isFocused = true;
        }
      }
      Component.onCompleted: {
        /* Initialize the viewer with the first loaded element of the model */
        if(index == listView.currentIndex) {
          viewerWrapper.viewer.source = path
          isFocused = true
          /* This may only occur when complete() is manually called : after a filtering */
          if(isSelected) selectedPictures.model.setProperty(name, "index", index);
        }
      }
    }
  }

  /* Define delegate for the view */
  Rectangle {
    id: dragIndicator

    anchors.top: separator2.bottom
    color: borderColor
    height: 2
    visible: false
    width: pictureWidget.width
  }

  /* Slots */
  function picturesMoved(indexFrom, indexTo){
    Utils.refreshModel();
    listView.currentIndex = indexTo;
    listView.currentItem.isFocused = true;
    viewerWrapper.viewer.source = listView.currentItem.imagePath
    selectedPictures.model.clear();
  }

  function picturesFiltered(){
    Utils.refreshModel();
    /* Repaint the viewer if needed */
    if(listView.currentItem){ 
      listView.currentItem.Component.completed();
    } else {
      viewerWrapper.viewer.source = "";
    }
  }
}
