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

  color: "#161616"
  width: Screen.desktopAvailableWidth - 300
  height: 600 //Screen.desktopAvailableHeight

  /*
   * All signals and slot are aliased here. Thus, they are easier to catch in PyQt, and are gather 
   * for reading purpose 
   */

  /* PICTURE COMPONENT SIGNALS/SLOTS */
  signal sig_movePictures(variant indexes, int indexTo)
  signal sig_discardPictures(variant indexes)
  signal sig_filterPictures(int status)
  function slot_picturesMoved(indexFrom, indexTo) { pictureManager.picturesMoved(indexFrom, indexTo); mapViewer.refresh() }
  function slot_picturesFiltered() { pictureManager.picturesFiltered(); mapViewer.refresh() }
  function slot_picturesDiscarded() { pictureManager.picturesDiscarded(); mapViewer.refresh() }

  /* RECONSTRUCTION COMPONENT SIGNALS/SLOTS */
  signal sig_launchReconstruction
  function slot_addLog(logDate, logMessage) { reconstruction.addLog(logDate, logMessage) }

  /* FETCHER COMPONENT SIGNALS/SLOTS */
  signal sig_importPictures(variant picturesFiles)
  function slot_picturesImported(pictureModel) { 
    pictureManager.pictures = pictureModel;
    pictureManager.picturesImported();
    mapViewer.pictures = pictureModel;
    var center = pictureModel.computeCenter();
    mapViewer.centerLatitude = center.latitude;
    mapViewer.centerLongitude = center.longitude;
  }

  /* CONFIGBAR SIGNALS/SLOTS */
  signal sig_changeShowMap(bool checked)
  signal sig_changeQuickConfig(bool checked)
  signal sig_changeActiveMode(bool checked)

  /* WORKSPACEMANAGER WIDGET SIGNALS/SLOTS */
  signal sig_newWorkspace(string name, string path)
  signal sig_openWorkspace(string path)
  signal sig_closeWorkspace(string path)
  signal sig_changeWorkspace(string path)
  signal sig_saveWorkspace(string name, string path)
  signal sig_deleteWorkspace(string path)

  signal sig_newScene(string name)
  signal sig_changeScene(string path)
  signal sig_deleteScene(string path)
  signal sig_importThumbnails()

  /* CAMERAINFO SIGNALS/SLOTS */
  function slot_cameraConnection(cameraConnected) { cameraInfo.isConnected = cameraConnected; }

  /* The menubar should rather be exported as a proper component */
  menuBar: Menu {
    id: menu
    // workspace signals
    onSig_menu_newWorkspace:    {newWorkspaceDialog.open()}
    onSig_menu_openWorkspace:   {openWorkspaceDialog.open()}
    onSig_menu_closeWorkspace:  {closeWorkspaceDialog.open()}
    onSig_menu_changeWorkspace: {changeWorkspaceDialog.open()}
    onSig_menu_saveWorkspace:   {saveWorkspaceDialog.open()}
    onSig_menu_deleteWorkspace: {deleteWorkspaceDialog.open()}
    // scene signals
    onSig_menu_newScene:        {newSceneDialog.open()}
    onSig_menu_changeScene:     {changeSceneDialog.open()}
    onSig_menu_deleteScene:     {deleteSceneDialog.open()}
    onSig_menu_importPictures:  {pictureFetcher.open()}
    onSig_menu_launchReconstruction:  {sig_launchReconstruction()}
    onSig_menu_importPictures:  { pictureFetcher.open() }
    onSig_menu_importThumbnails: sig_importThumbnails()
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

  GridLayout {
    width: parent.width
    height: parent.height
    columns: 3
    rows: 4
    columnSpacing: 0

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
      onFocusOnPicture: {
        mapViewer.centerLatitude = latitude
        mapViewer.centerLongitude = longitude
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
      showMapDefault: mapViewerDefaultVisible
    }

    Item {
      id: cameraInfo
      property alias isConnected: textCameraInfo.isConnected
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
        text: "TODO Timeline"
      }
    }

    Rectangle {
      id: renderer
      color: "transparent"
      Layout.fillHeight: true
      Layout.fillWidth: true
      Layout.minimumWidth: 300
      Layout.columnSpan: mapViewer.visible ? 1 : 2
      PointCloud{
        pathPly: "/home/matthieu/GIT/ENSEEIHT/3A/PL_POPART/MATRIX_ref/MatrixGUI/Components/QML/3dRendering/testOpenGLUnderQML/ply/castle.ply"
      }
    }

    MapViewer {
      id: mapViewer
      visible: mapViewerDefaultVisible
      Layout.fillHeight: true
      Layout.minimumWidth: root.width / 3
      Layout.maximumWidth: root.width / 3
    }
  }

  /* Temporary button to manually import pictures */
  /* A Window for the picture */
  PictureFetcher {
    id: pictureFetcher
    onImportPictures: sig_importPictures(picturesFiles)
  }
}
