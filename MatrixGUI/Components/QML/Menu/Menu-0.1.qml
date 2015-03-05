import QtQuick 2.0
import QtQuick.Controls 1.3
import QtQuick.Controls.Styles 1.3

MenuBar {

  /************ Workspace signals *************/
  signal sig_menu_newWorkspace()
  signal sig_menu_openWorkspace()
  signal sig_menu_closeWorkspace()
  signal sig_menu_changeWorkspace()
  signal sig_menu_saveWorkspace()
  signal sig_menu_deleteWorkspace()
  /************** Scene signals ***************/
  signal sig_menu_newScene()
  signal sig_menu_changeScene()
  signal sig_menu_deleteScene()
  signal sig_menu_importPictures()
  signal sig_menu_launchReconstruction()
  signal sig_menu_importThumbnails()

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
    MenuItem { text: "New workspace";     onTriggered: sig_menu_newWorkspace() }
    MenuItem { text: "Open workspace";    onTriggered: sig_menu_openWorkspace() }
    MenuItem { text: "Close workspace";   onTriggered: sig_menu_closeWorkspace() }
    MenuItem { text: "Change workspace";  onTriggered: sig_menu_changeWorkspace() }
    MenuItem { text: "Save workspace";    onTriggered: sig_menu_saveWorkspace() }
    MenuItem { text: "Delete workspace";  onTriggered: sig_menu_deleteWorkspace() }
  }
  Menu {
    title: "Scene"
    MenuItem { text: "New scene";    shortcut: "Ctrl+N"; onTriggered: sig_menu_newScene() }
    MenuItem { text: "Change scene";                     onTriggered: sig_menu_changeScene() }
    MenuItem { text: "Delete scene"; shortcut: "Ctrl+D"; onTriggered: sig_menu_deleteScene() }
    Menu { 
      title: "Import Pictures"
      MenuItem { text: "From computer...";  onTriggered: sig_menu_importPictures()  }
      MenuItem { text: "From camera..."; onTriggered: sig_menu_importThumbnails() }
    }
    MenuItem { text: "Launch 3D reconstruction";         onTriggered: sig_menu_launchReconstruction()}
  }

} 
