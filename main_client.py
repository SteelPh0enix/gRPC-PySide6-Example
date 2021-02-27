# This Python file uses the following encoding: utf-8
import sys
import os
import logging

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import Property, QObject, Signal, Slot

from client_libs import grpc_client


class GUIController(QObject):
    def __init__(self, parent):
        super().__init__(parent)
        self.grpc_client = None
        self._connection_status_value = 'Disconnected'

    def _connection_status(self):
        return self._connection_status_value

    def set_connection_status(self, new_status):
        self._connection_status_value = new_status
        self.connectionStatusChanged.emit(new_status)

    responseReceived = Signal(int, str, str)
    responseError = Signal(str)
    connectionStatusChanged = Signal(str)

    connectionStatus = Property(
        str, _connection_status, notify=connectionStatusChanged)

    def check_connection_status(self) -> bool:
        if self.grpc_client is None:
            self.set_connection_status(
                'Disconnected - connect to server before sending messages!')
            return False
        return True

    @Slot(str)
    def sendMessageGetMessage(self, message: str):
        if self.check_connection_status():
            try:
                response_id, response_timestamp, response_message = self.grpc_client.send_message_receive_message(
                    message)
                self.responseReceived.emit(
                    response_id, str(response_timestamp), response_message)

            except Exception as e:
                self.responseError.emit(
                    'Communication error - check stdout for details')
                print(e)
                return

    @Slot(str)
    def sendMessageGetStream(self, message: str):
        if self.check_connection_status():
            pass

    @Slot(str)
    def sendStreamGetMessage(self, message: str):
        if self.check_connection_status():
            pass

    @Slot(str)
    def sendStreamGetStream(self, message: str):
        if self.check_connection_status():
            pass

    @Slot(str, str)
    def connectToServer(self, ip: str, port: str):
        self.set_connection_status('Connecting...')
        if ip is None or port is None or len(ip) < 7 or len(port) == 0:
            self.set_connection_status('Invalid IP or port! Disconnected.')
            return

        self.grpc_client = grpc_client.GRPCClient(ip, port)
        # Try to send a message to server, to check if the client has connected successfully
        try:
            self.grpc_client.send_message_receive_message('')
        except RuntimeError as connection_error:
            self.set_connection_status(str(connection_error))
            del self.grpc_client
            self.grpc_client = None
            return
        except Exception as e:
            self.set_connection_status(
                'Unknown error occurred while connecting, check stdout for details')
            del self.grpc_client
            self.grpc_client = None
            print(e)
            return

        self.set_connection_status('Connected!')


def main():
    app = QGuiApplication(sys.argv)

    controller = GUIController(app)

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty('uiController', controller)
    engine.load(os.path.join(os.path.dirname(__file__), "main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())


if __name__ == "__main__":
    logging.basicConfig()
    main()
