import QtQuick 2.0
import QtQuick.Window 2.2
import QtQuick.Controls 1.3
import PictureWidget 1.0
import ReconstructionWidget 0.1
import MenuWidget 0.1
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
  signal sig_movePicture(int indexFrom, int indexTo)
  signal sig_discardPicture(int indexDelete)
  signal sig_filterPictures(int status)
  function slot_pictureMoved(index) { pictureWidget.pictureMoved(index) }
  function slot_picturesFiltered() { pictureWidget.picturesFiltered() }

  /* RECONSTRUCTION COMPONENT SIGNALS/SLOTS */
  signal sig_launchReconstruction
  function slot_addLog(logDate, logMessage) { reconstructionWidget.addLog(logDate, logMessage) }

  /* FETCHER COMPONENT SIGNALS/SLOTS */
  signal sig_importPictures(variant picturesFiles)
  function slot_picturesImported(pictureModel) { pictureWidget.pictures = pictureModel }

  /* The menubar should rather be exported as a proper component */
  menuBar: MenuWidget {
    id: menuWidget
  }

  /* May need a wrapper, we'll see later */
  PictureWidget {
    id: pictureWidget
    anchors.top: parent.top
    anchors.bottom: parent.bottom
    onMovePicture: sig_movePicture(indexFrom, indexTo)
    onFilterPictures: sig_filterPictures(status)
    onDiscardPicture: sig_discardPicture(indexDelete)
  }


  /* Wrapper for the reconstruction widget */
  Item {
    id: wrapperReconstruction
    width: root.width - pictureWidget.width
    height: reconstructionWidget.height
    anchors.left: pictureWidget.right
    ReconstructionWidget {
      id: reconstructionWidget
      onLaunchReconstruction: sig_launchReconstruction()
    }
  }

  /* A Window for the picture */
  PictureFetcher {
    id: pictureFetcher
    onImportPictures: sig_importPicture(picturesFiles)
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
