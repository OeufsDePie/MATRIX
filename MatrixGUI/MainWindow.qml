import QtQuick 2.0
import QtQuick.Window 2.2
import QtQuick.Controls 1.3
import PictureWidget 1.0
import ReconstructionWidget 0.1
import MenuWidget 0.1
import QtQuick.Dialogs 1.2         // for the FileDialog
import QtQuick.Layouts 1.1

ApplicationWindow {
  id: root
  color: "#161616"
  width: 800  //Screen.desktopAvailableWidth
  height: 600 //Screen.desktopAvailableHeight

  property alias pictures: pictureWidget.pictures

  /*
   * All signals and slot are aliased here. Thus, they are easier to catch in PyQt, and are gather 
   * for reading purpose 
   */

  /* PICTURE WIDGET SIGNALS/SLOTS */
  signal sig_pictureMoved
  signal sig_pictureDiscarded

  /* RECONSTRUCTION WIDGET SIGNALS/SLOTS */
  signal sig_launchReconstruction
  function slot_addLog(logDate, logMessage) { reconstructionWidget.addLog(logDate, logMessage) }

  /* WORKSPACEMANAGER WIDGET SIGNALS/SLOTS */
  signal sig_newWorkspace(string name, string path)
  signal sig_changeWorkspace()
  signal sig_deleteWorkspace()
  signal sig_newScene()
  signal sig_changeScene()
  signal sig_saveScene()
  signal sig_deleteScene()

  /* The menubar should rather be exported as a proper component */
  menuBar: MenuWidget {
    id: menuWidget
    // workspace signals
    onSig_menu_newWorkspace:    {newWorkspaceDialog.open()}
    onSig_menu_changeWorkspace: sig_changeWorkspace()
    onSig_menu_deleteWorkspace: sig_deleteWorkspace()
    // scene signals
    onSig_menu_newScene:        sig_newScene()
    onSig_menu_changeScene:     sig_changeScene()
    onSig_menu_saveScene:       sig_saveScene()
    onSig_menu_deleteScene:     sig_deleteScene()
  }

  Dialog {
    id: newWorkspaceDialog
    GridLayout{
      columns: 2
      Button{text: "Select Folder"; onClicked: selectFolderDialog.open()}
      Text{id: folderSelected; text: ""}
      Text{text: "Choose workspace name* :"}
      TextField{
        id: workspaceName;
        placeholderText: qsTr("Enter workspace name");
        selectByMouse: true
      }
      Text{text: "*The name will be used to generate\nthe workspace repository"}
    }
    standardButtons: StandardButton.Ok
    onAccepted: {
      sig_newWorkspace(workspaceName.text, folderSelected.text + "/" + workspaceName.text)
    }

    FileDialog {
      id: selectFolderDialog
      title: "Please choose a folder"
      selectFolder: true
      onAccepted: {
        var absolutePath = selectFolderDialog.folder.toString().substring(7)
        console.log("You chose: " + absolutePath)
        folderSelected.text = absolutePath
        //sig_newWorkspace("Workspace 3", absolutePath + "/Workspace_3")
      }
      onRejected: {console.log("Canceled")}
      visible: false
    }

  }

  /* May need a wrapper, we'll see later */
  PictureWidget {
    id: pictureWidget
    anchors.top: parent.top
    anchors.bottom: parent.bottom
    onPictureDiscarded: sig_pictureDiscarded()
    onPictureMoved: sig_pictureMoved()
    pictures: pictureModel
  }

  /* Wrapper for the reconstruction widget */
  Rectangle {
    width: root.width - pictureWidget.width
    anchors.left: pictureWidget.right
    ReconstructionWidget {
      id: reconstructionWidget
      onLaunchReconstruction: sig_launchReconstruction()
    }
  }

  /* Temporary model for test, ideally, it should be supplied via context by the PyQt script */
  ListModel {
    id: pictureModel
    ListElement{pictureIndex: 0; icon: "../../../Resources/Icons/processed.png"; status: "3"; name: "100_7100.JPG"; image: "../../../../ImageDataset_SceauxCastle/images/100_7100.JPG"}
    ListElement{pictureIndex: 1; icon: "../../../Resources/Icons/new.png"; status: "0"; name: "100_7101.JPG"; image: "../../../../ImageDataset_SceauxCastle/images/100_7101.JPG"}
    ListElement{pictureIndex: 2; icon: "../../../Resources/Icons/new.png"; status: "0"; name: "100_7102.JPG"; image: "../../../../ImageDataset_SceauxCastle/images/100_7102.JPG"}
    ListElement{pictureIndex: 3; icon: "../../../Resources/Icons/delete.png"; status: "2"; name: "100_7103.JPG"; image: "../../../../ImageDataset_SceauxCastle/images/100_7103.JPG"}
    ListElement{pictureIndex: 4; icon: "../../../Resources/Icons/processed.png"; status: "3"; name: "100_7104.JPG"; image: "../../../../ImageDataset_SceauxCastle/images/100_7104.JPG"}
    ListElement{pictureIndex: 5; icon: "../../../Resources/Icons/processed.png"; status: "3"; name: "100_7105.JPG"; image: "../../../../ImageDataset_SceauxCastle/images/100_7105.JPG"}
    ListElement{pictureIndex: 6; icon: "../../../Resources/Icons/processed.png"; status: "3"; name: "100_7106.JPG"; image: "../../../../ImageDataset_SceauxCastle/images/100_7106.JPG"}
    ListElement{pictureIndex: 7; icon: "../../../Resources/Icons/processed.png"; status: "3"; name: "100_7107.JPG"; image: "../../../../ImageDataset_SceauxCastle/images/100_7107.JPG"}
    ListElement{pictureIndex: 8; icon: "../../../Resources/Icons/reconstruction.png"; status: "1"; name: "100_7108.JPG"; image: "../../../../ImageDataset_SceauxCastle/images/100_7108.JPG"}
    ListElement{pictureIndex: 8; icon: "../../../Resources/Icons/new.png"; status: "0"; name: "100_7109.JPG"; image: "../../../../ImageDataset_SceauxCastle/images/100_7109.JPG"}
    ListElement{pictureIndex: 9; icon: "../../../Resources/Icons/processed.png"; status: "3"; name: "100_7110.JPG"; image: "../../../../ImageDataset_SceauxCastle/images/100_7110.JPG"}
  }

}
