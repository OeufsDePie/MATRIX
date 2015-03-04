import QtQuick 2.0
import QtQuick.Dialogs 1.2
import QtQuick.Controls 1.3
import QtQuick.Layouts 1.1

Dialog {
  id: changeWorkspaceDialog
  property alias model: combo.model
  ColumnLayout {
    anchors.left: parent.left
    anchors.right: parent.right
    spacing: 2
    Text{text: "Select the workspace :"}
    ComboBox {
      id: combo
      textRole: "display"
      Layout.fillWidth: true
    }
  }
  standardButtons: StandardButton.Cancel | StandardButton.Ok
  onAccepted: {
    sig_changeWorkspace(combo.currentText)
  }
}
