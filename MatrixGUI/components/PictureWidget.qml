import QtQuick 2.0
import QtQuick.XmlListModel 2.0
import QtQuick.Controls 1.3 

Item {
	id: pictureWidget
  property alias pictureModel: listView.model

	width: 300
	height: 700

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
		width: pictureWidget.width + 2
		height: pictureWidget.height - viewerWrapper.height - 25
		anchors.top: viewerWrapper.bottom

		ScrollView {
			anchors.fill: parent
			anchors.right: parent.right
			anchors.top: parent.top
			ListView {
				id: listView
				property int draggedItemIndex: -1
				delegate: pictureDelegate
				highlight: highlightDelegate
				highlightMoveDuration: 0
				currentIndex: 0
				boundsBehavior: Flickable.StopAtBounds
				interactive: true
				footer: Rectangle{
					width: 300
					height: 5
					color: "#dddddd"
				}
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
			/* Handle mouseClick in order to update the pictureViewer */
			MouseArea {
				id: dragArea
				anchors.fill: parent
				property int positionStarted
				property int positionEnded
				property int indexMoved: Math.floor((positionEnded - positionStarted)/pictureWrapper.height)
				onPressed: {
					positionStarted = pictureWrapper.y
					positionEnded = positionStarted
					dragArea.drag.target = pictureWrapper
				}
				onPositionChanged: {
					pictureWrapper.opacity = 0.5
					positionEnded = pictureWrapper.y
				}
				onReleased: {
					pictureWrapper.opacity = 1
					dragArea.drag.target = null
					pictureWrapper.y = positionStarted
					var newIndex = index + indexMoved
					newIndex = Math.max(0, newIndex >= pictureModel.count ? pictureModel.count - 1 : newIndex)
					console.log(positionStarted + "-> " + positionEnded + " = #" +indexMoved)
					if (indexMoved != 0) {
						pictureModel.move(index, newIndex, 1)
					} else {
						listView.currentIndex = index
						viewer.source = image
						console.log("Clicked on : " + index)
					}
				}
				drag.axis: Drag.YAxis
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
