import QtQuick 2.0
import QtQuick.XmlListModel 2.0
import QtQuick.Controls 1.3 

Rectangle {
	id: pictureWidget
	property alias pictureModel: listView.model
	
  /* Raised each time a picture is re-ordered */
  signal pictureMoved(int indexFrom, int indexTo)
  /* Raised when a picture is deleted/discarded */
  signal pictureDiscarded(int index)

	width: 300
  color: "blue"

  Component.onCompleted: {
    console.log(height)
  }
	/* First element is only a little picture viewer, as a box that contains an image  */
	Rectangle {
		id: viewerWrapper
		width: pictureWidget.width 
		height: width
		Image {
			id: viewer
			anchors.fill: parent
			anchors.centerIn: parent
			fillMode: Image.PreserveAspectCrop
			sourceSize.width: 2 * viewerWrapper.width
			clip: true
		}
	}

	/* Then is the complete list of pictures, only names are displayed */
  Item {
    anchors.top: viewerWrapper.bottom
		height: pictureWidget.height - viewerWrapper.height 
		width: pictureWidget.width 

		/* ScrollView will easily handle the data overflow */
    ScrollView {
      id: scrollView 

      anchors.fill: parent
 
      Component.onCompleted: {
        console.log(parent.height)
      }
      
      ListView {
        id: listView

				property int draggedItemIndex: -1

        anchors.fill: parent
				boundsBehavior: Flickable.StopAtBounds
				currentIndex: 0
        delegate: pictureDelegate
				highlight: highlightDelegate
				highlightMoveDuration: 0
			}
		}
	}

	/* Define delegate for the view */
	Component {
		id: pictureDelegate
		Item {
			id: pictureWrapper
			property variant picture: pictureModel
			
			height: pictureName.height
      width: pictureWidget.width
      /* Initialize the viewer with the first loaded element of the model */
			Component.onCompleted: {
				if(index == listView.currentIndex)
					viewer.source = image
			}
			Text {
				id: pictureName
				anchors.top: parent.top
				text: name
				color: "#000000"
			}
			/* Handle mouseClick in order to update the pictureViewer. Also
				in charge of reordering element via drag'n'drop	*/

			MouseArea {
				id: dragArea

				/* Properties use to handle the drag and drop */
				property int positionStarted
				property int positionEnded
				property int indexMoved: Math.floor((positionEnded - positionStarted)/pictureWrapper.height)

				anchors.fill: parent
				drag.axis: Drag.YAxis
				
				onPressed: {
					positionStarted = pictureWrapper.y
					/* Sounds glitchy, but we also initialize the positionEnded to handle simpleClick for which,
						onPositionChanged never get called */
					positionEnded = positionStarted
					dragArea.drag.target = pictureWrapper
				}
				onPositionChanged: {
					pictureWrapper.opacity = 0.5
					positionEnded = pictureWrapper.y
				}
				/* On release, click or move element, depending of the executed action */
				onReleased: {
					pictureWrapper.opacity = 1
					dragArea.drag.target = null
					pictureWrapper.y = positionStarted
					/* indexMoved == 0 means that the item wasn't drag, so it's considered as a click */
					if (indexMoved != 0) {
						/* Element has been dragged, let's move it */
						var newIndex = index + indexMoved
						/* Make sure that the computed index doesn't go out of bounds [0; model.count - 1]  */
						newIndex = Math.max(0, newIndex >= pictureModel.count ? pictureModel.count - 1 : newIndex)
						pictureModel.move(index, newIndex, 1)
            /* Send the corresponding signal */
            pictureMoved(index, newIndex)
					} else {
					  /* Only a click, so select the element in the viewer */
						listView.currentIndex = index
						viewer.source = image
					}
				}
			}
		}
	}

	/* Define delegate for the highlightning */
	Component {
		id: highlightDelegate
		Rectangle {
			color: "#1db7ff"
			y: listView.currentItem.y
		}
	}
}
