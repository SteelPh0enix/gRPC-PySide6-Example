# This Python file uses the following encoding: utf-8
import sys
import os
import logging
import threading
from typing import Callable, Iterator

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import Property, QCoreApplication, QObject, Signal, Slot
from google.protobuf.timestamp_pb2 import Timestamp

from client_libs import grpc_client


class ThreadedStreamHandler(threading.Thread):
    response_iterator = None
    response_data_lock = threading.Lock()
    data_handler = None
    transmission_exception = None

    def set_response_iterator(self, response_iterator: Iterator) -> None:
        self.response_iterator = response_iterator

    def set_data_handler(self, data_handler: Callable) -> None:
        self.data_handler = data_handler

    def run(self) -> None:
        if self.response_iterator is None:
            return

        self.response_data_lock.acquire()

        try:
            for response in self.response_iterator:
                self.data_handler(response)
        except Exception as e:
            self.transmission_exception = e

        del self.response_iterator
        self.response_iterator = None
        self.response_data_lock.release()


class GUIController(QObject):
    def __init__(self, parent):
        super().__init__(parent)
        self.grpc_client = None
        self._connection_status_value = 'Disconnected'

    def _connection_status(self) -> str:
        return self._connection_status_value

    def set_connection_status(self, new_status: str) -> None:
        self._connection_status_value = new_status
        self.connectionStatusChanged.emit(new_status)

    def parse_timestamp(self, timestamp: Timestamp) -> float:
        return timestamp.seconds + (timestamp.nanos / 10**9)

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
                logging.error(e)

    @Slot(str)
    def sendMessageGetStream(self, message: str):
        if self.check_connection_status():
            try:
                response_iterator = self.grpc_client.send_message_receive_stream(
                    message)

            #     for response in response_iterator:
            #         self.responseReceived.emit(response.id, self.parse_timestamp(
            #             response.timestamp), response.message)
            #         QCoreApplication.processEvents()

                stream_handler = ThreadedStreamHandler()
                stream_handler.set_response_iterator(response_iterator)
                stream_handler.set_data_handler(lambda response: self.responseReceived.emit(
                    response.id, self.parse_timestamp(response.timestamp), response.message))
                stream_handler.start()
                print('thread started')

                while stream_handler.response_data_lock.acquire(blocking=True, timeout=0.05) == False:
                    print('processEvents')
                    QCoreApplication.processEvents()

                stream_handler.response_data_lock.release()
                print('done')

                if stream_handler.transmission_exception is not None:
                    raise stream_handler.transmission_exception

            except Exception as e:
                self.responseError.emit(
                    'Communication error - check stdout for details')
                logging.error(e)

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
            logging.error(e)
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
    logging.basicConfig(level=logging.DEBUG)
    main()
