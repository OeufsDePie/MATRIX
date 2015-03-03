import QtQuick 2.0
import QtQuick.Window 2.2
import QtQuick.Controls 1.3
import PictureManager 1.0
import Reconstruction 0.1
import Menu 0.1
import PictureFetcher 0.1
import NewWorkspaceDialogWidget 0.1

ApplicationWindow {
  id: root
  color: "#161616"
  width: 800  //Screen.desktopAvailableWidth
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

  /* WORKSPACEMANAGER WIDGET SIGNALS/SLOTS */
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

  /* May need a wrapper, we'll see later */
  PictureManager {
    id: pictureManager
    anchors.top: parent.top
    anchors.bottom: parent.bottom
    onMovePictures: sig_movePictures(indexes, indexTo)
    onFilterPictures: sig_filterPictures(status)
    onDiscardPicture: sig_discardPicture(indexDelete)
  }


  /* Wrapper for the reconstruction widget */
  Item {
    id: wrapperReconstruction
    width: root.width - pictureManager.width
    height: reconstruction.height
    anchors.left: pictureManager.right
    Reconstruction {
      id: reconstruction
      onLaunchReconstruction: sig_launchReconstruction()
    }
  }

  /* A Window for the picture */
  PictureFetcher {
    id: pictureFetcher
    onImportPictures: sig_importPictures(picturesFiles)
  }

  /* Temporary button to manually import pictures */
  Rectangle {
    width: 200
    height: 50
    color: "#1db7ff"
    anchors.top: wrapperReconstruction.bottom
    anchors.horizontalCenter: wrapperReconstruction.horizontalCenter
    Text {
      anchors.centerIn: parent
      text: "Import Pictures"
      color: "white"
    }
    MouseArea {
      anchors.fill: parent
      onPressed: pictureFetcher.open()
    }
  }
}
