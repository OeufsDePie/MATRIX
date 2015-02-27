import QtQuick 2.0
import QtQuick.Dialogs 1.2

FileDialog {
  id: selectFolderDialog
  property var target: ""
  title: "Please choose a folder"
  selectFolder: true
  onAccepted: {
    var absolutePath = selectFolderDialog.folder.toString().substring(7)
    console.log("You chose: " + absolutePath)
    target.text = absolutePath
  }
  onRejected: {console.log("Canceled")}
  visible: false
}
