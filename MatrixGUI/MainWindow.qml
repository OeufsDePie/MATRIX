import QtQuick 2.0
import QtQuick.Window 2.2
import QtQuick.Controls 1.3
import QtQuick.Layouts 1.1

import PictureManager 1.0
import Reconstruction 0.1
import Menu 0.1
import PictureFetcher 0.1
import NewWorkspaceDialogWidget 0.1
import ConfigBar 0.1

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
  function slot_picturesImported(pictureModel) { pictureManager.pictures = pictureModel }

  /* CONFIGBAR SIGNALS/SLOTS */
  signal sig_changeShowMap(bool checked)
  signal sig_changeQuickConfig(bool checked)
  signal sig_changeActiveMode(bool checked)

  /* WORKSPACEMANAGER WIDGET SIGNALS/SLOTS */
  signal sig_newWorkspace(string name, string path)
  signal sig_changeWorkspace()
  signal sig_deleteWorkspace()
  signal sig_newScene()
  signal sig_changeScene()
  signal sig_saveScene()
  signal sig_deleteScene()  /* WORKSPACEMANAGER WIDGET SIGNALS/SLOTS */
  signal sig_newWorkspace(string name, string path)
  signal sig_changeWorkspace()
  signal sig_deleteWorkspace()
  signal sig_newScene()
  signal sig_changeScene()
  signal sig_saveScene()
  signal sig_deleteScene()

  /* The menubar should rather be exported as a proper component */
  menuBar: Menu {
    id: menu
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

  NewWorkspaceDialogWidget {
    id: newWorkspaceDialog
  }

  GridLayout {
    width: parent.width
    height: parent.height
    columns: 30
    rows: 30
    PictureManager {
      id: pictureManager
      width: 300
      Layout.columnSpan: 10
      Layout.rowSpan: 30
      Layout.fillHeight: true
      onMovePictures: sig_movePictures(indexes, indexTo)
      onFilterPictures: sig_filterPictures(status)
      onDiscardPicture: sig_discardPicture(indexDelete)
    } 
    ConfigBar {
      id: configBar
      Layout.columnSpan: 20
      Layout.rowSpan: 10
      Layout.fillHeight: true
      Layout.alignment: Qt.AlignHCenter

      onChangeShowMap: sig_changeShowMap(checked)
      onChangeQuickConfig: sig_changeQuickConfig(checked)
      onChangeActiveMode: sig_changeActiveMode(checked)
    }

    /* Import Button */
    Rectangle {
      width: 200
      height: 50
      color: "#1db7ff"
      Text {
        anchors.centerIn: parent
        text: "Import Pictures"
        color: "white"
      }
      MouseArea {
        anchors.fill: parent
        onPressed: pictureFetcher.open()
      }
      Layout.alignment: Qt.AlignHCenter
      Layout.columnSpan: 20
      Layout.rowSpan: 5
    }
  }


  /* Temporary button to manually import pictures */
  /* A Window for the picture */
  PictureFetcher {
    id: pictureFetcher
    onImportPictures: sig_importPictures(picturesFiles)
  }
}