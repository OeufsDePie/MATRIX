import QtQuick 2.0
import QtQuick.Controls 1.3 

ComboBox {
  model: ListModel {
    ListElement { text: "All";            value: -1 }
    ListElement { text: "New";            value: 0 }
    ListElement { text: "Reconstruction"; value: 1 }
    ListElement { text: "Processed";      value: 3 }
    ListElement { text: "Discarded";      value: 2 }
  }
}