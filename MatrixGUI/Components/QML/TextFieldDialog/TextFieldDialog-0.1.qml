import QtQuick 2.0
import QtQuick.Dialogs 1.2
import QtQuick.Controls 1.3
import QtQuick.Layouts 1.1

Dialog {
  id: textFieldDialog
  property alias label: label.text
  property alias placeholder: input.placeholderText
  property alias input: input.text
  property alias complementaryInfo: complementaryInfo.text
  width: dialogGrid.implicitWidth + 20
  GridLayout{
    id: dialogGrid
    width: 700
    columns: 2
    columnSpacing: 15
    anchors.left: parent.left
    anchors.right: parent.right
    Text{id: label}
    TextField{
      id: input;
      selectByMouse: true;
      Layout.fillWidth: true
    }
    Text{id: complementaryInfo; Layout.columnSpan: 2}
  }
  standardButtons: StandardButton.Cancel | StandardButton.Ok
}
