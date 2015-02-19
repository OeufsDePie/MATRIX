import QtQuick 2.0
import QtQuick.Controls 1.2 
import QtQuick.Window 2.2
import QtQuick.Controls.Styles 1.3
import "components"


ApplicationWindow {
	id: root
	width: 800  //Screen.desktopAvailableWidth
	height: 600 //Screen.desktopAvailableHeight
	
	/* The menubar should rather be exported as a proper component */
	menuBar: MenuBar {
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

  /* Temporary model for test, ideally, it should be supplied via context by the PyQt script */
	ListModel {
		id: pictureModel
		ListElement {name: "little_kitten"; image: "/home/mbenkort/Documents/ProjeyLong/MatrixGUI/pictures/image-chaton-549-1920-1200.php.jpeg"}
		ListElement {name: "Alexis Ren"; image: "/home/mbenkort/Download/tumblr_mape1203Z01qjldjvo1_500.png"}
		ListElement {name: "Fantome Pacman"; image: "/home/mbenkort/Download/Pacman 3.png"}
		ListElement {name: "little_kitten"; image: "/home/mbenkort/Documents/ProjeyLong/MatrixGUI/pictures/image-chaton-549-1920-1200.php.jpeg"}
		ListElement {name: "Alexis Ren"; image: "/home/mbenkort/Download/tumblr_mape1203Z01qjldjvo1_500.png"}
		ListElement {name: "Fantome Pacman"; image: "/home/mbenkort/Download/Pacman 3.png"}
		ListElement {name: "little_kitten"; image: "/home/mbenkort/Documents/ProjeyLong/MatrixGUI/pictures/image-chaton-549-1920-1200.php.jpeg"}
		ListElement {name: "Alexis Ren"; image: "/home/mbenkort/Download/tumblr_mape1203Z01qjldjvo1_500.png"}
		ListElement {name: "Fantome Pacman"; image: "/home/mbenkort/Download/Pacman 3.png"}
		ListElement {name: "little_kitten"; image: "/home/mbenkort/Documents/ProjeyLong/MatrixGUI/pictures/image-chaton-549-1920-1200.php.jpeg"}
		ListElement {name: "Alexis Ren"; image: "/home/mbenkort/Download/tumblr_mape1203Z01qjldjvo1_500.png"}
		ListElement {name: "Fantome Pacman"; image: "/home/mbenkort/Download/Pacman 3.png"}
		ListElement {name: "little_kitten"; image: "/home/mbenkort/Documents/ProjeyLong/MatrixGUI/pictures/image-chaton-549-1920-1200.php.jpeg"}
		ListElement {name: "Alexis Ren"; image: "/home/mbenkort/Download/tumblr_mape1203Z01qjldjvo1_500.png"}
		ListElement {name: "Fantome Pacman"; image: "/home/mbenkort/Download/Pacman 3.png"}
		ListElement {name: "little_kitten"; image: "/home/mbenkort/Documents/ProjeyLong/MatrixGUI/pictures/image-chaton-549-1920-1200.php.jpeg"}
		ListElement {name: "Alexis Ren"; image: "/home/mbenkort/Download/tumblr_mape1203Z01qjldjvo1_500.png"}
		ListElement {name: "Fantome Pacman"; image: "/home/mbenkort/Download/Pacman 3.png"}
	}

	/* May need a wrapper, we'll see later */
	PictureWidget {
		id: pictureWidget
		anchors.left: parent.left
		height: root.height
		pictureModel: pictureModel
	}

	/* Wrapper for the reconstruction widget */
	Rectangle {
		width: root.width - pictureWidget.width
		anchors.left: pictureWidget.right
		ReconstructionWidget {}
	}

}
