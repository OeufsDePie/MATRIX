import QtQuick 2.0
import QtQuick.Controls 1.3
import QtQuick.Controls.Styles 1.3

MenuBar {

  /************ Workspace signals *************/
  signal sig_menu_newWorkspace()
  signal sig_menu_changeWorkspace()
  signal sig_menu_deleteWorkspace()
  /************** Scene signals ***************/
  signal sig_menu_newScene()
  signal sig_menu_changeScene()
  signal sig_menu_saveScene()
  signal sig_menu_deleteScene()

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
    MenuItem { text: "New workspace";    onTriggered: sig_menu_newWorkspace() }
    MenuItem { text: "Change workspace"; onTriggered: sig_menu_changeWorkspace() }
    MenuItem { text: "Delete workspace"; onTriggered: sig_menu_deleteWorkspace() }
  }
  Menu {
    title: "Scene"
    MenuItem { text: "New scene";    shortcut: "Ctrl+N"; onTriggered: sig_menu_newScene() }
    MenuItem { text: "Change scene";                     onTriggered: sig_menu_changeScene() }
    MenuItem { text: "Save scene";   shortcut: "Ctrl+S"; onTriggered: sig_menu_saveScene() }
    MenuItem { text: "Delete scene"; shortcut: "Ctrl+D"; onTriggered: sig_menu_deleteScene() }
  }

} 
