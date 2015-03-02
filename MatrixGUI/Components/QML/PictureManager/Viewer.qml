import QtQuick 2.0

Rectangle {
  property alias viewer: _viewer

  Image {
    id: _viewer
    anchors {fill: parent; centerIn: parent}
    clip: true
    fillMode: Image.PreserveAspectCrop
    sourceSize.width: 2 * parent.width
  }
}