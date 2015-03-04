import QtQuick 2.0
import QtQuick.Dialogs 1.2

FileDialog {
  id: selectFileDialog
  selectFolder: false
  selectMultiple: false
  onRejected: {console.log("Canceled")}
  visible: false
}

