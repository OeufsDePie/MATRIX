import QtQuick 2.0
import QtQuick.Window 2.2
import QtQuick.Controls 1.3
import PictureWidget 1.0
import ReconstructionWidget 0.1
import MenuWidget 0.1

ApplicationWindow {
  id: root
  color: "#161616"
  width: 800  //Screen.desktopAvailableWidth
  height: 600 //Screen.desktopAvailableHeight

  property alias pictures: pictureWidget.pictureModel

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

  /* The menubar should rather be exported as a proper component */
  menuBar: MenuWidget {}

  /* May need a wrapper, we'll see later */
  PictureWidget {
    id: pictureWidget
    anchors.top: parent.top 
    anchors.bottom: parent.bottom
    pictureModel: pictureModel
    onPictureDiscarded: sig_pictureDiscarded()
    onPictureMoved: sig_pictureMoved()
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
    ListElement{name: "100_7100.JPG"; image: "../../../ImageDataset_SceauxCastle/images/100_7100.JPG"}
    ListElement{name: "100_7101.JPG"; image: "../../../ImageDataset_SceauxCastle/images/100_7101.JPG"}
    ListElement{name: "100_7102.JPG"; image: "../../../ImageDataset_SceauxCastle/images/100_7102.JPG"}
    ListElement{name: "100_7103.JPG"; image: "../../../ImageDataset_SceauxCastle/images/100_7103.JPG"}
    ListElement{name: "100_7104.JPG"; image: "../../../ImageDataset_SceauxCastle/images/100_7104.JPG"}
    ListElement{name: "100_7105.JPG"; image: "../../../ImageDataset_SceauxCastle/images/100_7105.JPG"}
    ListElement{name: "100_7106.JPG"; image: "../../../ImageDataset_SceauxCastle/images/100_7106.JPG"}
    ListElement{name: "100_7107.JPG"; image: "../../../ImageDataset_SceauxCastle/images/100_7107.JPG"}
    ListElement{name: "100_7108.JPG"; image: "../../../ImageDataset_SceauxCastle/images/100_7108.JPG"}
    ListElement{name: "100_7109.JPG"; image: "../../../ImageDataset_SceauxCastle/images/100_7109.JPG"}
    ListElement{name: "100_7110.JPG"; image: "../../../ImageDataset_SceauxCastle/images/100_7110.JPG"}
  }

}
