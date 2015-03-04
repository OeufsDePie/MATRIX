import QtQuick 2.0
import QtQuick.Window 2.2
import QtQuick.Controls 1.3
import QtQuick.Layouts 1.1

import PictureManager 1.0
import Reconstruction 0.1
import Menu 0.1
import PictureFetcher 0.1
import NewWorkspaceDialogWidget 0.1
import SelectFileDialog 0.1
import SelectFromModelDialog 0.1
import ConfigBar 0.1
import MapViewer 0.1

ApplicationWindow {
  id: root

  color: "#161616"
  width: Screen.desktopAvailableWidth
  height: 600 //Screen.desktopAvailableHeight

  /*
   * All signals and slot are aliased here. Thus, they are easier to catch in PyQt, and are gather 
   * for reading purpose 
   */

  /* PICTURE COMPONENT SIGNALS/SLOTS */
  signal sig_movePictures(variant indexes, int indexTo)
  signal sig_discardPicture(int indexDelete)
  signal sig_filterPictures(int status)
  function slot_picturesMoved(indexFrom, indexTo) { pictureManager.picturesMoved(indexFrom, indexTo) }
  function slot_picturesFiltered() { pictureManager.picturesFiltered() }

  /* RECONSTRUCTION COMPONENT SIGNALS/SLOTS */
  signal sig_launchReconstruction
  function slot_addLog(logDate, logMessage) { reconstruction.addLog(logDate, logMessage) }

  /* FETCHER COMPONENT SIGNALS/SLOTS */
  signal sig_importPictures(variant picturesFiles)
  function slot_picturesImported(pictureModel) { 
    pictureManager.pictures = pictureModel;
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
  signal sig_saveWorkspace()
  signal sig_deleteWorkspace(string path)

  signal sig_newScene()
  signal sig_changeScene()
  signal sig_deleteScene()

  /* The menubar should rather be exported as a proper component */
  menuBar: Menu {
    id: menu
    // workspace signals
    onSig_menu_newWorkspace:    {newWorkspaceDialog.open()}
    onSig_menu_openWorkspace:   {openWorkspaceDialog.open()}
    onSig_menu_closeWorkspace:  {closeWorkspaceDialog.open()}
    onSig_menu_changeWorkspace: {changeWorkspaceDialog.open()}
    onSig_menu_saveWorkspace:   {sig_saveWorkspace()}
    onSig_menu_deleteWorkspace: {deleteWorkspaceDialog.open()}
    // scene signals
    onSig_menu_newScene:        {sig_newScene()}
    onSig_menu_changeScene:     {sig_changeScene()}
    onSig_menu_deleteScene:     {sig_deleteScene()}
    onSig_menu_importPictures:  {pictureFetcher.open()}
  }

  NewWorkspaceDialogWidget {
    id: newWorkspaceDialog
  }
  SelectFileDialog {
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
  SelectFromModelDialog { // delete workspace
    id: deleteWorkspaceDialog
    model: workspacesModel       // transfered from orchestrator.py
    title: "Select workspace to delete :"
    onAccepted: {sig_deleteWorkspace(deleteWorkspaceDialog.selected)}
  }

  GridLayout {
    width: parent.width
    height: parent.height
    columns: 3
    rows: 3
    columnSpacing: 0

    PictureManager {
      id: pictureManager
      Layout.rowSpan: 3
      Layout.fillHeight: true
      Layout.minimumWidth: 300
      onMovePictures: sig_movePictures(indexes, indexTo)
      onFilterPictures: sig_filterPictures(status)
      onDiscardPicture: sig_discardPicture(indexDelete)
      onFocusOnPicture: {
        mapViewer.centerLatitude = latitude
        mapViewer.centerLongitude = longitude
      }
    } 
    ConfigBar {
      id: configBar
      Layout.columnSpan: 2
      Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
      Layout.minimumHeight: 40
      onChangeShowMap: {
        sig_changeShowMap(checked)
        mapViewer.visible = checked
      }
      onChangeQuickConfig: sig_changeQuickConfig(checked)
      onChangeActiveMode: sig_changeActiveMode(checked)
      showMapDefault: mapViewerDefaultVisible
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
      color: "#020202"
      Layout.fillHeight: true
      Layout.fillWidth: true
      Layout.minimumWidth: 300
      Layout.columnSpan: mapViewer.visible ? 1 : 2
      Text {
        anchors.centerIn: parent
        color: "#ffffff"
        text: "TODO Renderer"
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
