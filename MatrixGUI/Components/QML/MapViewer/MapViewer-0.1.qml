import QtQuick 2.0
import QtLocation 5.3
import QtPositioning 5.2

Item {
  id: mapViewer

  signal focusOnPicture(int index)

  property variant pictures
  property real centerLatitude
  property real centerLongitude
  property int focused

  Map {
    id: map
    anchors.fill: parent
    /* Using Open Street Map Plugin to display map info */
    plugin: Plugin { name: "osm" }
    center {
      latitude: centerLatitude
      longitude: centerLongitude
    }

    gesture.enabled: true
    Component.onCompleted: zoomLevel = 17

    MapItemView {
      id: itemView
      model: pictures
      delegate: pin
    }
  }

  Component {
    id: pin
    MapCircle {
      id: circle
      property bool isFocused: mapViewer.focused == index
      property alias isHovered: mouseArea.containsMouse
      border.width: 0
      color: circleColor
      center {
        latitude: latitude
        longitude: longitude
      }
      /* Quelle est donc cette sorcellerie O_o */
      radius: 0.6 * Math.pow(2, (Math.max(1, 20 - map.zoomLevel))) * (isFocused || isHovered ? 2 : 1)
      MouseArea {
        id: mouseArea

        anchors.fill: parent
        hoverEnabled: true
        onClicked: {
          mapViewer.focused = index;
          focusOnPicture(index);
        }

        cursorShape: (containsMouse ? Qt.PointingHandCursor : Qt.ArrowCursor);
      }
    }
  }

  function refresh(){
    itemView.model = pictures;
  }

  function reset(){
    itemView.model = []; 
  }
}
