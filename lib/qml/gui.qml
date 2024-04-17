import QtQuick 2.0
import QtQuick.Layouts 1.11
import QtQuick.Controls 2.1
import QtQuick.Window 2.1
import QtQuick.Controls.Material 2.1
import QtQuick.Dialogs

import io.qt.textproperties 1.0

ApplicationWindow {
    id: page
    width: 500
    height: 200
    minimumWidth: 500
    minimumHeight: 200
    visible: true
    Material.theme: Material.Dark
    Material.accent: Material.Purple
    title: qsTr("CSV Combiner")
    CSVCombiner {
        id: csvCombiner
    }
    FolderDialog {
        id: folderDialog
        onAccepted: {
            status.text = csvCombiner.combineCSV(currentFolder, delimiter.text)
        }
    }

    ColumnLayout {
        anchors.fill: parent
        Layout.alignment: Qt.AlignTop
        TextArea{
            id: delimiter
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            placeholderText: "delimiter"
        }
        Button {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            text: "Select Folder"
            onClicked: {
                if (delimiter.text!=="") {
                    folderDialog.open()
                }
                else {
                    status.text = "please enter a delimiter"
                }
            }
        }
        Text {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            id: status
            color: "pink"
            text: ""
        }
    }
}