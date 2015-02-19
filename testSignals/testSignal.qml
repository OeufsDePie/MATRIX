import QtQuick 2.0

Rectangle {
	id: myComponent
	signal myQmlSignal
	signal triggerMySignal

	color: "#161616"

	width: 640
	height: 480

	Column {
		spacing: 10
		anchors.centerIn: parent

		Row {
			spacing: 10
			Rectangle {
				id: button1

				width: 150
				height: 50
				color: "#1db7ff"

				Text {
					anchors.centerIn: parent;
					color: "white"
					text: "Send a Signal"
				}
				MouseArea {
					anchors.fill: parent
					onClicked: myQmlSignal()
				}
			}
			Rectangle {
				id: button2

				width: 150
				height: 50
				color: "#1db7ff"
				Text {
					anchors.centerIn: parent;
					color: "white"
					text: "Ask for a Signal"
				}
				MouseArea {
					anchors.fill: parent
					onClicked: triggerMySignal()
				}
			}
		}

		Text {
			id: myText
			color: "white"
		}
	}

	function myQmlSlot(message) {
		myText.text = message
	}
}

