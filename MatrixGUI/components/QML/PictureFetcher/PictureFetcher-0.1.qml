import QtQuick 2.0
import QtQuick.Dialogs 1.0

/*
 * This view is a dialog box used when the user has to select several photos to import.
 * It will breed the pictureManager with the imported pictures
 */
FileDialog {
  id: fileDialog

 // property alias selectedFolder: fileDialog.folder
  folder: "/home/mbenkort/Documents/ProjeyLong/MATRIX/MatrixGUI/Workspace"
  selectMultiple: true
  selectFolder: false
  nameFilters: ["Image files (*.jpg *.png *.jpeg *.JPEG, *.JPG, *.PNG)"]
  title: "If you could choose pictures to import, that would be great."
  onAccepted: {
    console.log(fileDialog.fileUrls)
    Qt.quit()
  }
  Component.onCompleted: visible = true
}
