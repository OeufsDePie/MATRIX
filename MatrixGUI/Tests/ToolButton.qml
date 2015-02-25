import QtQuick 2.0
import QtQuick.Controls 1.3

Item {
  width: 800
  height: 600

  ToolBar {
    anchors.bottom: parent.bottom
    tools: ToolBarLayout {
      ToolButton {
        iconSource: "toolbar-back"
      }
    }
  }
}
