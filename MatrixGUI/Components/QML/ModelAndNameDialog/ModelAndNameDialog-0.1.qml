import QtQuick 2.0
import QtQuick.Dialogs 1.2
import QtQuick.Controls 1.3
import QtQuick.Layouts 1.1

Dialog {
  id: modelAndNameDialog
  property alias nameLabel: nameLabel.text
  property alias namePlaceholder: name.placeholderText
  property alias complementaryInfo: complementaryInfo.text
  property alias name: name.text
  property alias model: combo.model
  property alias selected: combo.currentText
  width: dialogGrid.implicitWidth + 20
  GridLayout{
    id: dialogGrid
    width: 700
    columns: 2
    columnSpacing: 15
    anchors.left: parent.left
    anchors.right: parent.right
    ComboBox {
      id: combo
      textRole: "display"
      Layout.fillWidth: true
      Layout.columnSpan: 2
    }
    Text{id: nameLabel}
    TextField{
      id: name;
      selectByMouse: true;
      Layout.fillWidth: true
    }
    Text{id: complementaryInfo; Layout.columnSpan: 2}
  }
  standardButtons: StandardButton.Cancel | StandardButton.Ok
}
