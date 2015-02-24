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
		title: "Project"
		MenuItem { text: "Quit" }
	}
	
 } 
