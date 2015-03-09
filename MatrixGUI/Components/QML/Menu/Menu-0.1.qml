import QtQuick 2.0
import QtQuick.Controls 1.3
import QtQuick.Controls.Styles 1.3

MenuBar {
  property bool workspaceAvailable

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
  signal sig_menu_confirmThumbnails()
  
  style: MenuBarStyle{
    background: Rectangle {
      color: "#cccccc"
    } 
  } 

  Menu {
    title: "Workspace"
    MenuItem { text: "New workspace";     onTriggered: sig_menu_newWorkspace(); shortcut: "Ctrl+Shift+N"; }
    MenuItem { text: "Open workspace";    onTriggered: sig_menu_openWorkspace() }
    MenuItem { text: "Close workspace";   onTriggered: sig_menu_closeWorkspace();   enabled: workspaceAvailable}
    MenuItem { text: "Change workspace";  onTriggered: sig_menu_changeWorkspace();  enabled: workspaceAvailable}
    MenuItem { text: "Save workspace";    onTriggered: sig_menu_saveWorkspace();    enabled: workspaceAvailable; shortcut: "Ctrl+S" }
    MenuItem { text: "Delete workspace";  onTriggered: sig_menu_deleteWorkspace();  enabled: workspaceAvailable}
  }
  Menu {
    title: "Scene"
    enabled: workspaceAvailable
    MenuItem { text: "New scene";    shortcut: "Ctrl+N"; onTriggered: sig_menu_newScene() }
    MenuItem { text: "Change scene";                     onTriggered: sig_menu_changeScene() }
    MenuItem { text: "Delete scene"; shortcut: "Ctrl+D"; onTriggered: sig_menu_deleteScene() }
    Menu { 
      title: "Import Pictures"
      MenuItem { text: "From computer...";  onTriggered: sig_menu_importPictures()  }
      MenuItem { text: "From camera..."; onTriggered: sig_menu_importThumbnails() }
    }
  }
  Menu {
    title: "Tools"
    enabled: workspaceAvailable
    MenuItem { text: "Confirm thumbnails"; onTriggered: sig_menu_confirmThumbnails() }
    MenuItem { text: "Launch 3D reconstruction"; onTriggered: sig_menu_launchReconstruction()}
  }
} 
