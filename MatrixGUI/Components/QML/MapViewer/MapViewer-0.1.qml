import QtQuick 2.0
import QtLocation 5.3
import QtPositioning 5.2

Item {
  id: mapViewer

  property variant pictures
  property real centerLatitude
  property real centerLongitude

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
      border.width: 0
      color: "#1db7ff"
      center {
        latitude: latitude
        longitude: longitude
      }
      radius: latitude == map.center.latitude && longitude == map.center.longitude ? 10 : 5
    }
  }

  function refresh(){
    itemView.model = pictures;
  }

  function reset(){
    itemView.model = []; 
  }
}
