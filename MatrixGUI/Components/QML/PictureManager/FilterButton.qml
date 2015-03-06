import QtQuick 2.0
import QtQuick.Controls 1.3 

ComboBox {
  model: ListModel {
    ListElement { text: "All";            value: 101}
    ListElement { text: "Discarded";      value: 102}
    ListElement { text: "New";            value: 0 }
    ListElement { text: "Processed";      value: 3 }
    ListElement { text: "Reconstruction"; value: 1 }
    ListElement { text: "Rejected";       value: 2 }
    ListElement { text: "Thumbnails";     value: 4 }
    ListElement { text: "Valid";          value: 103}
  }
}