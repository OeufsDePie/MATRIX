import QtQuick 2.0
import QtQuick.Dialogs 1.2
import QtQuick.Controls 1.3
import QtQuick.Layouts 1.1
import FolderDialogWidget 0.1

Dialog {
  id: folderAndNameDialog
  property alias nameLabel: nameLabel.text
  property alias namePlaceholder: name.placeholderText
  property alias complementaryInfo: complementaryInfo.text
  property alias folder: folderSelected.text
  property alias name: name.text
  width: dialogGrid.implicitWidth + 20
  GridLayout{
    id: dialogGrid
    width: 700
    columns: 2
    columnSpacing: 15
    anchors.left: parent.left
    anchors.right: parent.right
    Button{text: "Select Folder"; onClicked: selectFolderDialog.open(); Layout.fillWidth: true}
    Text{id: folderSelected; text: ""}
    Text{id: nameLabel}
    TextField{
      id: name;
      selectByMouse: true;
      Layout.fillWidth: true
    }
    Text{id: complementaryInfo; Layout.columnSpan: 2}
  }
  standardButtons: StandardButton.Cancel | StandardButton.Ok

  FolderDialogWidget {
    id: selectFolderDialog
    target: folderSelected
  }

}
