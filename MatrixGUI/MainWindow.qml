import QtQuick 2.0
import QtQuick.Window 2.2
import QtQuick.Controls 1.3
import QtQuick.Layouts 1.1

import PictureManager 1.0
import Reconstruction 0.1
import Menu 0.1
import PictureFetcher 0.1
import FolderAndNameDialog 0.1
import SelectFileDialog 0.1
import SelectFromModelDialog 0.1
import ModelAndNameDialog 0.1
import TextFieldDialog 0.1
import ConfigBar 0.1
import MapViewer 0.1
import PointCloud 1.0

ApplicationWindow {
  id: root

  property bool workspaceAvailable: false

  color: "#161616"
  width: 1000
  height: 600 //Screen.desktopAvailableHeight
  title: "MATRIX"
  /*
   * All signals and slot are aliased here. Thus, they are easier to catch in PyQt, and are gather 
   * for reading purpose 
   */

  /* PICTURE COMPONENT SIGNALS/SLOTS */
  signal sig_movePictures(variant indexes, int indexTo)
  signal sig_deletePictures(variant indexes)
  signal sig_discardPictures(variant indexes)
  signal sig_renewPictures(variant indexes)
  signal sig_filterPictures(int status)
  function slot_picturesUpdated(pictures) { 
    pictureManager.picturesUpdated(pictures);
    mapViewer.pictures = pictures;
    var center = pictures.computeCenter();
    mapViewer.centerLatitude = center.latitude;
    mapViewer.centerLongitude = center.longitude;
    mapViewer.refresh()
  }
  /* RECONSTRUCTION COMPONENT SIGNALS/SLOTS */
  signal sig_launchReconstruction()
  function slot_reconstructionChanged(plyPath) {
    Qt.createQmlObject("import QtQuick 2.0; import PointCloud 1.0; 
      PointCloud {
        pathPly: '" + plyPath + "'
      }"
    , renderer);
  }

  /* FETCHER COMPONENT SIGNALS/SLOTS */
  signal sig_importPictures(variant picturesFiles)

  /* CONFIGBAR SIGNALS/SLOTS */
  signal sig_changeShowMap(bool checked)
  signal sig_changeQuickConfig(bool checked)
  signal sig_changeActiveMode(bool checked)

  /* WORKSPACEMANAGER WIDGET SIGNALS/SLOTS */
  signal sig_newWorkspace(string name, string path)
  signal sig_openWorkspace(string path)
  signal sig_closeWorkspace(string path)
  signal sig_changeWorkspace(string path)
  signal sig_saveWorkspace()
  signal sig_deleteWorkspace(string path)
  function slot_workspaceAvailable(status) { root.workspaceAvailable = status }

  signal sig_newScene(string name)
  signal sig_changeScene(string path)
  signal sig_deleteScene(string path)
  signal sig_importThumbnails()
  signal sig_confirmThumbnails()

  /* CAMERAINFO SIGNALS/SLOTS */
  function slot_cameraConnection(cameraConnected, name) { 
    cameraInfo.isConnected = cameraConnected; 
    cameraInfo.name = name;
  }

  /* The menubar should rather be exported as a proper component */
  menuBar: Menu {
    id: menu

    workspaceAvailable: root.workspaceAvailable

    // workspace signals
    onSig_menu_newWorkspace:    {newWorkspaceDialog.open()}
    onSig_menu_openWorkspace:   {openWorkspaceDialog.open()}
    onSig_menu_closeWorkspace:  {closeWorkspaceDialog.open()}
    onSig_menu_changeWorkspace: {changeWorkspaceDialog.open()}
    onSig_menu_saveWorkspace:   sig_saveWorkspace()
    onSig_menu_deleteWorkspace: {deleteWorkspaceDialog.open()}

    // scene signals
    onSig_menu_newScene:        {newSceneDialog.open()}
    onSig_menu_changeScene:     {changeSceneDialog.open()}
    onSig_menu_deleteScene:     {deleteSceneDialog.open()}
    onSig_menu_importPictures:  {pictureFetcher.open()}
    onSig_menu_importThumbnails: sig_importThumbnails()
    onSig_menu_launchReconstruction: sig_launchReconstruction()
    onSig_menu_confirmThumbnails: sig_confirmThumbnails()
  }

  FolderAndNameDialog { // create a new workspace
    id: newWorkspaceDialog
    nameLabel: "Choose workspace name* :"
    namePlaceholder: qsTr("Enter workspace name")
    complementaryInfo: "*The name will be used to generate the workspace repository"
    onAccepted: {sig_newWorkspace(name, folder)}
  }
  SelectFileDialog { // open a saved workspace
    id: openWorkspaceDialog
    title: "Choose the file corresponding to the workspace save"
    onAccepted: {
      var absolutePath = openWorkspaceDialog.fileUrl.toString().substring(7)
      sig_openWorkspace(absolutePath)
    }
  }
  SelectFromModelDialog { // change workspace
    id: changeWorkspaceDialog
    model: workspacesModel       // transfered from orchestrator.py
    title: "Select workspace :"
    onAccepted: {sig_changeWorkspace(changeWorkspaceDialog.selected)}
  }
  SelectFromModelDialog { // close workspace
    id: closeWorkspaceDialog
    model: workspacesModel       // transfered from orchestrator.py
    title: "Select workspace to close :"
    onAccepted: {sig_closeWorkspace(closeWorkspaceDialog.selected)}
  }
  ModelAndNameDialog { // save the workspace
    id: saveWorkspaceDialog
    nameLabel: "Choose a name for the save"
    namePlaceholder: qsTr("Enter save name")
    complementaryInfo: ""
    model: workspacesModel       // transfered from orchestrator.py
    onAccepted: {sig_saveWorkspace(name, selected)}
  }
  SelectFromModelDialog { // delete workspace
    id: deleteWorkspaceDialog
    model: workspacesModel       // transfered from orchestrator.py
    title: "Select workspace to delete :"
    onAccepted: {sig_deleteWorkspace(deleteWorkspaceDialog.selected)}
  }
  TextFieldDialog { // create a new scene
    id: newSceneDialog
    label: "Choose a name for the new scene*"
    placeholder: qsTr("name")
    complementaryInfo: "* The name will be used to generate the scene path inside the current workspace"
    onAccepted: {sig_newScene(input)}
  }
  SelectFromModelDialog { // change scene
    id: changeSceneDialog
    model: scenesModel       // transfered from orchestrator.py
    title: "Select a scene :"
    onAccepted: {sig_changeScene(changeSceneDialog.selected)}
  }
  SelectFromModelDialog { // delete a scene
    id: deleteSceneDialog
    model: scenesModel       // transfered from orchestrator.py
    title: "Select a scene to delete :"
    onAccepted: {sig_deleteScene(deleteSceneDialog.selected)}
  }

  Text {
    id: textWelcome1
    anchors.horizontalCenter: parent.horizontalCenter
    anchors.top: parent.top
    anchors.topMargin: root.height / 4
    text: "Welcome in MATRIX\nan MVG Assitant Tool for Reconstruction from Images eXtraction"
    font.pixelSize: 17
    font.bold: true
    horizontalAlignment: Text.AlignHCenter
    color: "#ffffff"
    visible: !root.workspaceAvailable
  }

  Text {
    id: textWelcome2
    anchors.top: textWelcome1.top
    anchors.topMargin: root.height / 3
    anchors.horizontalCenter: parent.horizontalCenter
    text: "Please, create a workspace or select an existing one to start working."
    font.pixelSize: 14
    horizontalAlignment: Text.AlignHCenter
    color: "#ffffff"
    visible: !root.workspaceAvailable
  }

  GridLayout {
    id: appContent
    columns: 3
    columnSpacing: 0
    height: parent.height
    rows: 4
    visible: root.workspaceAvailable
    width: parent.width

    PictureManager {
      id: pictureManager
      Layout.rowSpan: 4
      Layout.fillHeight: true
      Layout.minimumWidth: 300
      onMovePictures: {
        mapViewer.reset();
        sig_movePictures(indexes, indexTo);
      }
      onFilterPictures: {
        mapViewer.reset();
        sig_filterPictures(status);
      }
      onDiscardPictures: {
        mapViewer.reset();
        sig_discardPictures(indexes);
      }
      onDeletePictures: {
        mapViewer.reset();
        sig_deletePictures(indexes);
      }
      onRenewPictures: {
        mapViewer.reset();
        sig_renewPictures(indexes);
      }
      onFocusOnPicture: {
        mapViewer.centerLatitude = latitude
        mapViewer.centerLongitude = longitude
        mapViewer.focused = index
      }
    } 
    ConfigBar {
      id: configBar
      Layout.columnSpan: 2
      Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
      onChangeShowMap: {
        sig_changeShowMap(checked)
        mapViewer.visible = checked
      }
      onChangeQuickConfig: sig_changeQuickConfig(checked)
      onChangeActiveMode: sig_changeActiveMode(checked)
      showMapDefault: false
    }

    Item {
      id: cameraInfo
      property alias isConnected: textCameraInfo.isConnected
      property alias name: textCameraName.text

      Layout.columnSpan: 2
      Layout.fillWidth: true
      height: textCameraInfo.height
      RowLayout {
        anchors.centerIn: parent
        spacing: 10
        Text {
          color: "#ffffff"
          text: "Camera connected : "
        }
        Text {
          id: textCameraInfo
          property bool isConnected: false
          color: isConnected ? "#98cd00" : "#ff3237"
          text: isConnected ? "Yes :)" : "No :'("
          font.bold: true
        }
        Item { width: 100 }
        Text {
          color: "#ffffff"
          text: "Camera : "
        }
        Text {
          id: textCameraName
          color: "#ffffff"
          text: "Unknown"
          font.bold: true
        }
      }
    }

    Rectangle {
      id: timeline
      Layout.columnSpan: 2
      Layout.fillWidth: true
      color: "#666666"
      height: 40
      Text {
        anchors.centerIn: parent
        color: "#ffffff"
        text: ""
      }
    }

    Rectangle {
      id: renderer
      color: "transparent"
      Layout.fillHeight: true
      Layout.fillWidth: true
      Layout.minimumWidth: 300
      Layout.columnSpan: mapViewer.visible ? 1 : 2
    }

    MapViewer {
      id: mapViewer
      visible: false
      Layout.fillHeight: true
      Layout.minimumWidth: root.width / 3
      Layout.maximumWidth: root.width / 3
      onFocusOnPicture: pictureManager.focusOnPictureMap(index);
    }
  }

  /* Temporary button to manually import pictures */
  /* A Window for the picture */
  PictureFetcher {
    id: pictureFetcher
    onImportPictures: sig_importPictures(picturesFiles)
  }
}
