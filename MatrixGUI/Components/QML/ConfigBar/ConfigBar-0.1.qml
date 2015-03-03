import QtQuick 2.0
import QtQuick.Layouts 1.1

RowLayout {
  id: configBar

  signal changeQuickConfig(bool checked)
  signal changeActiveMode(bool checked)
  signal changeShowMap(bool checked)

  property alias quickConfigDefault: quickConfig.checkedDefault
  property alias activeModeDefault: activeMode.checkedDefault
  property alias showMapDefault: showMap.checkedDefault

  spacing: 25

  ButtonToggable {
    id: quickConfig
    labelValue: "Quick Config"
    onValueChanged: changeQuickConfig(checked)
  }
  ButtonToggable {
    id: activeMode
    labelValue: "Active Mode"
    onValueChanged: changeActiveMode(checked)
  }

  ButtonToggable {
    id: showMap
    labelValue: "Show the map"
    onValueChanged: changeShowMap(checked)
  }

}