import QtQuick 2.0
import QtQuick.Dialogs 1.2
import QtQuick.Controls 1.3
import QtQuick.Layouts 1.1
import FolderDialogWidget 0.1

Dialog {
  id: newWorkspaceDialog
  width: dialogGrid.width + 20
  GridLayout{
   id: dialogGrid
   width: 700
   columns: 2
   columnSpacing: 15
   anchors.horizontalCenter: newWorkspaceDialog.anchors.horizontalCenter
   Button{text: "Select Folder"; onClicked: selectFolderDialog.open(); Layout.fillWidth: true}
   Text{id: folderSelected; text: ""}
   Text{text: "Choose workspace name* :"}
   TextField{
     id: workspaceName;
     placeholderText: qsTr("Enter workspace name");
     selectByMouse: true;
     Layout.fillWidth: true
   }
   Text{text: "*The name will be used to generate the workspace repository"; Layout.columnSpan: 2}
  }
  standardButtons: StandardButton.Ok
  onAccepted: {
   sig_newWorkspace(workspaceName.text, folderSelected.text + "/" + workspaceName.text)
  }

  FolderDialogWidget {
   id: selectFolderDialog
   target: folderSelected
  }

}
