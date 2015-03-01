import QtQuick 2.0
import QtQuick.Window 2.2
import QtQuick.Controls 1.3
import PictureManager 1.0
import Reconstruction 0.1
import Menu 0.1
import PictureFetcher 0.1

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

  /* The menubar should rather be exported as a proper component */
  menuBar: Menu {
    id: menu
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
