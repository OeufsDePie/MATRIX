import QtQuick 2.0
import QtQuick.Controls.Styles 1.3

Component {
  id: buttonStyle
  ButtonStyle {
    background: Rectangle {
        implicitWidth: control.width
        implicitHeight: control.height
        gradient: Gradient {
            GradientStop { position: 0 ; color: control.pressed ? borderColor : selectionColor }
            GradientStop { position: 1 ; color: selectionColor }
        }
        radius: 0
    }
    label: Item{
      anchors.fill: parent
      Text {
        anchors.centerIn: parent
        color: "#ffffff"
        text: control.text
        font.pointSize: 9
        font.bold: true
      }
    }
  }
}