import QtQuick 2.0
import QtQuick.Dialogs 1.2
import QtQuick.Controls 1.3
import QtQuick.Layouts 1.1

Dialog {
  id: selectFromModelDialog
  property alias model: combo.model
  property alias title: title.text
  property alias selected: combo.currentText
  ColumnLayout {
    anchors.left: parent.left
    anchors.right: parent.right
    spacing: 2
    Text{
      id: title;
    }
    ComboBox {
      id: combo
      textRole: "display"
      Layout.fillWidth: true
    }
  }
  standardButtons: StandardButton.Cancel | StandardButton.Ok
}
