import QtQuick 2.0
import QtQuick.Window 2.2
import QtQuick.Controls 1.3
import "components"

ApplicationWindow {
	id: root
	width: 800  //Screen.desktopAvailableWidth
	height: 600 //Screen.desktopAvailableHeight

	/* All signals and slot are aliased here. Thus, they are easier to catch in PyQt, and are gather 
	for reading purpose */

	/* PICTURE WIDGET SIGNALS/SLOTS */
  signal sig_picturesUpdated
	
	/* RECONSTRUCTION WIDGET SIGNALS/SLOTS */
	signal sig_launchReconstruction
	function slot_addLog(logDate, logMessage) { reconstructionWidget.addLog(logDate, logMessage) }
	
	/* The menubar should rather be exported as a proper component */
	menuBar: MenuBarWidget {}

	/* May need a wrapper, we'll see later */
	PictureWidget {
		id: pictureWidget
		anchors.left: parent.left
		height: root.height
		pictureModel: pictureModel
		onPicturesUpdated: sig_picturesUpdated()
	}

	/* Wrapper for the reconstruction widget */
	Rectangle {
		width: root.width - pictureWidget.width
		anchors.left: pictureWidget.right
		ReconstructionWidget {
			id: reconstructionWidget
			onLaunchReconstruction: sig_launchReconstruction()
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

}
