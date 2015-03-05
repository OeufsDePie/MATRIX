import QtQuick 2.0
import QtQuick.Controls.Styles 1.3

Component {
  id: comboBoxStyle
  ComboBoxStyle {
    background: Rectangle {
      implicitWidth: toolbar.buttonWidth
      implicitHeight: toolbar.buttonHeight
      gradient: Gradient {
          GradientStop { position: 0 ; color: control.pressed ? borderColor : pictureWidget.selectionColor }
          GradientStop { position: 1 ; color: pictureWidget.selectionColor }
      }
      radius: 0
      Item {
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        anchors.rightMargin: 5
        anchors.verticalCenter: parent.verticalCenter
        height: dropDown.height
        width: dropDown.width
        Text {
          id: dropDown
          text: "\u25BE"
          color: "#ffffff"
          font.pointSize: 10
        }
      }
    }
    label: Text {
      anchors.left: parent.left
      width: parent.width * 0.9
      clip: true
      color: "#ffffff"
      text: control.editText
      font.pointSize: 9
      font.bold: true
    }
    dropDownButtonWidth: 5
  }
}