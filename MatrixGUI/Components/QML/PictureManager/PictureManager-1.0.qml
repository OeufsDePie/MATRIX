import QtQuick 2.0
import QtQuick.Controls 1.3 
import QtQuick.Controls.Styles 1.3
import QtQuick.Layouts 1.1
import QtQuick.Dialogs 1.2

import "Utils.js" as Utils

Rectangle {
  id: pictureWidget

  /* Make it easier to configure */
  property string borderColor: "#76d2fe"
  property string selectionColor: "#1db7ff"
  property string textColor: "#000000"

  signal deletePictures(variant indexes) /* Raised when picture are deleted */
  signal discardPictures(variant indexes) /* Raised when a picture is discarded */
  signal filterPictures(int status) /* Raised when ordering a filter */
  signal focusOnPicture(real latitude, real longitude) /* Raised when clicking on a picture */
  signal movePictures(variant indexes, int indexTo) /* Raised each time a picture is re-ordered */
  signal renewPictures(variant indexes /* Raised each time a picture is renewed */)

  /* First element is only a little picture viewer, as a box that contains an image  */
  Viewer {
    id: viewerWrapper

    anchors {top: parent.top; left: parent.left}
    height: width
    width: pictureWidget.width 
  }

  /* Just a separator */
  Separator { id: separator1; anchors.top: viewerWrapper.bottom }

  /* Little toolbar */
  RowLayout {
    id: toolbar

    property int buttonWidth: (pictureWidget.width - toolbar.spacing) / 2
    property int buttonHeight: 25

    anchors.top: separator1.bottom
    spacing: 10
    anchors.horizontalCenter: parent.horizontalCenter
  
    /* Unselect all pictures easily */
    Button {
      id: unselectButton
      height: toolbar.buttonHeight
      style: MyButtonStyle {}
      text: "Unselect All"
      width: toolbar.buttonWidth
      onClicked: selectedPictures.model.clear();
    }

    /* Filtering button, to manage pictures visualisation easily */
    FilterButton {
      id: filterButton

      height: toolbar.buttonHeight
      style: MyComboBoxStyle {}
      width: toolbar.buttonWidth

      /* Filter all pictures below by triggering a signal */
      onCurrentIndexChanged: {
        filterPictures(filterButton.model.get(filterButton.currentIndex).value);
      }  
    }
  }

  /* Just another separator */
  Separator { id: separator2; anchors.top: toolbar.bottom }

  Item {
    id: selectedPictures
    /* This little object will be used to manage selections of pictures */
    property variant model: ListModel {}
  }

  /* Then is the complete list of pictures, only names are displayed */
  Item {
    id: listWrapper
    anchors {top: separator2.bottom; bottom: separator3.top }
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
        model: []
      }
    }
  }

  /* Just another separator */
  Separator { id: separator3; anchors.bottom: toolbar2.top }

  /* Little toolbar */
  RowLayout {
    id: toolbar2

    property int buttonWidth: (pictureWidget.width - 2*toolbar.spacing) / 3
    property int buttonHeight: toolbar.buttonHeight

    anchors.bottom: parent.bottom
    anchors.horizontalCenter: parent.horizontalCenter

    spacing: 10
  
    /* Discard a picture from the model */
    Button {
      id: discardButton
      height: toolbar2.buttonHeight
      style: MyButtonStyle {}
      text: "Discard"
      width: toolbar2.buttonWidth
      onClicked: discardPictures(Utils.selectedIndexes());
    }

    /* Renew a picture in the model */
    Button {
      id: renewButton
      height: toolbar2.buttonHeight
      style: MyButtonStyle {}
      text: "Renew"
      width: toolbar2.buttonWidth
      onClicked: renewPictures(Utils.selectedIndexes());
    }

    /* Delete a picture from the model */
    Button {
      id: deleteButton
      height: toolbar2.buttonHeight
      style: MyButtonStyle {}
      text: "Delete"
      width: toolbar2.buttonWidth + 1
      onClicked: confirmDelete.open()
    }
  }

  MessageDialog {
    id: confirmDelete
    informativeText: "This action will delete selected pictures files from the workspace."
    modality: Qt.ApplicationModal
    standardButtons: StandardButton.Yes | StandardButton.No
    title: "Take a time to breath"
    text: "Continue ?"
    onYes: deletePictures(Utils.selectedIndexes())
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
          viewerWrapper.viewer.source = path;
          isFocused = true;
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
  function picturesUpdated(pictures){
    selectedPictures.model.clear();
    listView.model = []; // Force a repaint
    listView.model = pictures;
    listView.currentIndex = 0;
    if(listView.currentItem){ 
      listView.currentItem.Component.completed();
    } else {
      viewerWrapper.viewer.source = "";
    }
  }
}
