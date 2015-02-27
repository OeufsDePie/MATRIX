import QtQuick 2.0
import QtQuick.Dialogs 1.0

/*
 * This view is a dialog box used when the user has to select several photos to import.
 * It will breed the pictureManager with the imported pictures
 */
FileDialog {
  id: fileDialog

  signal importPictures(variant picturesFiles)

  property alias selectedFolder: fileDialog.folder
  selectMultiple: true
  selectFolder: false
  nameFilters: ["Image files (*.jpg *.png *.jpeg *.JPEG, *.JPG, *.PNG)"]
  title: "If you could choose pictures to import, that would be great."
  Component.onCompleted: visible = true
  onAccepted: {
    importPictures(fileDialog.fileUrls)
  }
}
