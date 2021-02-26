# This Python file uses the following encoding: utf-8
import sys
import os

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Signal, Slot

class GUIController(QObject):
    def __init__(self, parent):
        super().__init__(parent)

    responseReceived = Signal(int, str, str)

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


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    controller = GUIController(app)

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty('uiController', controller)
    engine.load(os.path.join(os.path.dirname(__file__), "main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
