# This Python file uses the following encoding: utf-8
import sys
import os

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
    connectionStatusChanged = Signal(str)

    connectionStatus = Property(
        str, _connection_status, notify=connectionStatusChanged)

    @Slot(str)
    def sendMessageGetMessage(self, message: str):
        pass

    @Slot(str)
    def sendMessageGetStream(self, message: str):
        pass

    @Slot(str)
    def sendStreamGetMessage(self, message: str):
        pass

    @Slot(str)
    def sendStreamGetStream(self, message: str):
        pass

    @Slot(str, str)
    def connectToServer(self, ip: str, port: str):
        if ip is None or port is None or len(ip) < 7 or len(port) == 0:
            self.set_connection_status('Invalid IP or port!')
            return

        self.set_connection_status('Connecting...')
        self.grpc_client = grpc_client.GRPCClient(ip, port)


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    controller = GUIController(app)

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty('uiController', controller)
    engine.load(os.path.join(os.path.dirname(__file__), "main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
