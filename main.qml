import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Window {
    id: mainWindow
    width: 640
    height: 480
    visible: true
    title: qsTr("gRPC + PySide6 Example")

    ColumnLayout {
        id: mainWindowLayout
        anchors.fill: parent
        spacing: 5
        anchors.rightMargin: 10
        anchors.leftMargin: 10
        anchors.bottomMargin: 10
        anchors.topMargin: 10

        RowLayout {
            id: connectionFieldsLayout
            Layout.alignment: Qt.AlignLeft | Qt.AlignTop
            Layout.preferredHeight:  25
            Layout.fillWidth: true
            Layout.fillHeight: false

            TextField {
                id: grpcIPField
                placeholderText: qsTr("Server's IP address")
                Layout.fillWidth: true
            }

            TextField {
                id: grpcPortField
                placeholderText: qsTr("Server's port")
                Layout.fillWidth: true
            }

            Button {
                id: grpcConnectButton
                text: qsTr("Connect")
                Layout.preferredWidth: 100
            }
        }

        RowLayout {
            id: statusLayout
            Layout.alignment: Qt.AlignLeft | Qt.AlignTop
            Layout.preferredHeight: 30
            Layout.fillWidth: true
            Layout.fillHeight: false

            Label {
                id: statusLabel
                text: qsTr("Status:")
                font.pointSize: 12
            }

            Label {
                id: statusLabelValue
                text: qsTr("Disconnected")
                font.pointSize: 12
                font.bold: true
                Layout.fillWidth: true
            }
        }

        RowLayout {
            id: simpleMessageLayout
            Layout.alignment: Qt.AlignLeft | Qt.AlignTop

            TextField {
                id: textField
                placeholderText: qsTr("Text Field")
                Layout.fillWidth: true
            }

            Button {
                id: buttonSendSimpleMessage
                text: qsTr("Send simple message")
            }
        }
    }
}
