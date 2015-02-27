import QtQuick 2.0

/* Reconstruction widget handle all interactions with the user in order to launch the reconstruction. 
	 Temporary, it will display information about the recontruction such as generated .ply files */
Item {
	id: reconstructionWidget

	signal launchReconstruction

	width: parent.width
	height: 300

	/* The button that may launch the reconstruction */
	Rectangle {
		id: buttonWrapper
		anchors.horizontalCenter: parent.horizontalCenter
		anchors.top: parent.top
		color: "#1db7ff"
		height: 30
		width: buttonContent.width + 20
		Text {
			id: buttonContent
			anchors.centerIn: parent
			text: "Launch Reconstruction"
			color: "white"
		}
		MouseArea {
			anchors.fill: parent
			onClicked: {
				launchReconstruction()
			}
		}
	}

	/* Display all log message */
	Rectangle {
		height: reconstructionWidget.height - buttonWrapper.height 
		width: reconstructionWidget.width
		anchors.top: buttonWrapper.bottom
		color: "transparent"	
		ListView {
			id: recontructionLogsView
			model: reconstructionLogsModel
			delegate: reconstructionLogsDelegate
			anchors.fill: parent
			clip: true
		}
	}

	Component {
		id: reconstructionLogsDelegate
		Rectangle {
			color: "#eeeeee"
			width:  parent.width
			height: 20
			Text {
				text: date + " : " + message
				color: "#161616"
			}
		}
	}
  
	/* Handle logEntry as a ListModel */
	ListModel {
		id: reconstructionLogsModel 
	}
  
  
	/* Slot that manage the model/logs */
	function addLog(logDate, logMessage){
		reconstructionLogsModel.append({"date": logDate, "message": logMessage})
	}

}
