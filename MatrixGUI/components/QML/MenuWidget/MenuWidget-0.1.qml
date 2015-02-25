import QtQuick 2.0
import QtQuick.Controls 1.3
import QtQuick.Controls.Styles 1.3

MenuBar {
  style: MenuBarStyle{
    background: Rectangle {
      color: "#cccccc"
    } 
  } 

  Menu {
    title: "Home"
  }
  Menu {
    title: "Workspace"
    MenuItem { text: "New workspace" }
    MenuItem { text: "Change workspace" }
    MenuItem { text: "Delete workspace" }
  }
  Menu {
    title: "Scene"
    MenuItem { text: "New scene" }
    MenuItem { text: "Change scene" }
    MenuItem { text: "Save scene" }
    MenuItem { text: "Delete scene" }
  }

} 
