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

    function printLine(message) {
        responseTextArea.text += message + "\n"
    }

    function printResponse(id, timestamp, response) {
        var text_line = "Response #" + id + " @ " + timestamp + ": " + response + "\n"
        responseTextArea.text += text_line
    }

    Connections {
        id: responseConnection
        target: uiController

        function onResponseReceived(id, timestamp, data) {
            printResponse(id, timestamp, data)
        }

        function onResponseError(message) {
            printLine('[ERROR] ' + message)
        }
    }

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
            Layout.minimumHeight: 20
            Layout.maximumHeight: 30
            Layout.alignment: Qt.AlignLeft | Qt.AlignTop
            Layout.preferredHeight:  20
            Layout.fillWidth: true
            Layout.fillHeight: false

            TextField {
                id: grpcIPField
                placeholderText: qsTr("Server's IP address")
                text: qsTr("127.0.0.1")
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
                Layout.fillHeight: true
                Layout.preferredWidth: 100

                onClicked: {
                    uiController.connectToServer(grpcIPField.text, grpcPortField.text)
                }
            }
        }

        RowLayout {
            id: statusLayout
            Layout.minimumHeight: 40
            Layout.maximumHeight: 50
            Layout.alignment: Qt.AlignLeft | Qt.AlignTop
            Layout.preferredHeight: 50
            Layout.fillWidth: true
            Layout.fillHeight: false

            Label {
                id: statusLabel
                text: qsTr("Status:")
                font.pointSize: 12
            }

            Label {
                id: statusLabelValue
                text: uiController.connectionStatus
                font.pointSize: 12
                font.bold: true
                Layout.fillWidth: true
            }
        }

        TextField {
            id: simpleMessageField
            Layout.preferredHeight: 20
            Layout.maximumHeight: 20
            Layout.minimumHeight: 20
            placeholderText: qsTr("Message")
            Layout.fillWidth: true
        }

        ScrollView {
            id: responseTextAreaView
            Layout.fillHeight: true
            Layout.fillWidth: true

            TextArea {
                id: responseTextArea
                text: ""
                font.pointSize: 10
                placeholderText: qsTr("Server's responses")
                readOnly: true
            }
        }

        RowLayout {
            id: simpleMessageLayout
            Layout.minimumHeight: 25
            Layout.maximumHeight: 50
            Layout.preferredHeight: 50
            Layout.alignment: Qt.AlignLeft | Qt.AlignTop

            Button {
                id: buttonSendSimpleMessage
                text: qsTr("Message-to-message")
                Layout.fillHeight: true
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

                onClicked: {
                    uiController.sendMessageGetMessage(simpleMessageField.text)
                }
            }

            Button {
                id: buttonSendStreamingMessage
                text: qsTr("Message-to-stream")
                flat: false
                display: AbstractButton.TextOnly
                Layout.fillHeight: true
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

                onClicked: {
                    uiController.sendMessageGetStream(simpleMessageField.text)
                }
            }

            Button {
                id: buttonReceiveStreamingResponse
                text: qsTr("Stream-to-message")
                Layout.fillHeight: true
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

                onClicked: {
                    uiController.sendStreamGetMessage(simpleMessageField.text)
                }
            }

            Button {
                id: buttonStreamMessages
                text: qsTr("Stream-to-stream")
                Layout.fillHeight: true
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

                onClicked: {
                    uiController.sendStreamGetStream(simpleMessageField.text)
                }
            }
        }


    }
}
