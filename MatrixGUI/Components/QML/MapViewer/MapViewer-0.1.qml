import QtQuick 2.0
import QtLocation 5.3
import QtPositioning 5.2

Item {
  id: mapViewer
  width: 800
  height: 600

  Map {
    id: map
    anchors.fill: parent
    plugin: Plugin { 
      name: "nokia" 
      PluginParameter {name: "app_id"; value: "liygoHgPxa5gjJlMQ7F"}
      PluginParameter {name: "token"; value: "xsu2IGuSc_eN_BQfxT1o9w"}
      PluginParameter {name: "proxy"; value: "system"}
    }
    center {
      latitude: 43.36
      longitude: 1.26
    }

    gesture.enabled: true
  }
}
