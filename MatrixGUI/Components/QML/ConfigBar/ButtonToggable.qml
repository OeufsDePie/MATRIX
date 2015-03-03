import QtQuick 2.0
import QtQuick.Layouts 1.1

Item {
  id: buttonToggable

  signal valueChanged(bool checked)

  property string mainColor: "#1db7ff"
  property string textColor: "white"
  property string labelValue: ""
  property int easeDuration: 200
  property alias checkedDefault: cache.checked

  // height: wrapper.height
  // width: label.width + wrapper.spacing + buttonWrapper.width

  height: 30
  width: wrapper.spacing + label.width + buttonWrapper.width


  RowLayout {
    id: wrapper
    anchors.fill: parent
    spacing: height / 4
    Text {
      id: label
      color: textColor
      text: labelValue
    }

    Rectangle {
      id: buttonWrapper

      border {width: 2; color: mainColor}
      color: "transparent"
      height: wrapper.height
      width: 2 * (textOn.width + textOff.width)

      Item {
        id: on

        anchors.left: parent.left
        anchors.leftMargin: parent.border.width
        anchors.verticalCenter: parent.verticalCenter      
        height: parent.height - 2 * parent.border.width
        width: parent.width / 2 - parent.border.width

        Text {
          id: textOn

          anchors.centerIn: parent
          color:"white"
          text: "on"
        } 
      }

      Item {
        id: off

        anchors.left: on.right
        anchors.verticalCenter: parent.verticalCenter      
        height: parent.height - 2 * parent.border.width
        width: parent.width / 2 - parent.border.width

        Text {
          id: textOff

          anchors.centerIn: parent
          color:"white"
          text: "off"
        } 
      }

      Rectangle {
        id: cache
        property bool checked: true

        anchors.leftMargin: checked ? 0 : buttonWrapper.border.width
        anchors.verticalCenter: parent.verticalCenter
        color: mainColor
        height: parent.height - 2 * parent.border.width
        width: parent.width / 2 - parent.border.width

        states: [
          State {
            name: "checked"
            AnchorChanges { 
              target: cache
              anchors.left: on.right 

            }
          },
          State {
            name: "unchecked"
            AnchorChanges { 
              target: cache
              anchors.left: buttonWrapper.left 
            }
          }
        ]

        transitions: Transition {
          AnchorAnimation { duration: easeDuration }
        }

        Component.onCompleted: state = checked ? "checked" : "unchecked";

      }

      MouseArea {
        id: mouseArea

        anchors.fill: parent
        onClicked: {
          cache.state = ((cache.checked = !cache.checked) ? "checked" : "unchecked");
          valueChanged(cache.checked);
        }
      }
    }
  }
}