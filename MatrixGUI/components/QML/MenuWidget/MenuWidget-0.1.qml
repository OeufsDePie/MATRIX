import QtQuick 2.0
import QtQuick.Controls 1.3
import QtQuick.Controls.Styles 1.3

MenuBar {

  /************ Workspace signals *************
   * signal sig_newWorkspace()
   ********************************************/
  /************** Scene signals ***************
   * signal sig_newScene()
   ********************************************/

  id: menu
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
    MenuItem { text: "New workspace"; onTriggered: root.sig_newWorkspace() }
    MenuItem { text: "Change workspace" }
    MenuItem { text: "Delete workspace" }
  }
  Menu {
    title: "Scene"
    MenuItem { text: "New scene"; shortcut: "Ctrl+N"; onTriggered: root.sig_newScene() }
    MenuItem { text: "Change scene"}
    MenuItem { text: "Save scene"; shortcut: "Ctrl+S" }
    MenuItem { text: "Delete scene"; shortcut: "Ctrl+D" }
  }

} 
