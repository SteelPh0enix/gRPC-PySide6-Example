from typing import Tuple
from google.protobuf.timestamp_pb2 import Timestamp
from proto import ExampleService_pb2_grpc as example_grpc
from proto import ExampleService_pb2 as example_pb2
import grpc
import time


class GRPCClient():
    def __init__(self, ip, port):
        self.channel = grpc.insecure_channel(f'{ip}:{port}')
        self.stub = example_grpc.ExampleServiceStub(self.channel)
        self.message_id = 0

    def create_timestamp(self) -> Timestamp:
        now = time.time()
        seconds = int(now)
        nanos = int((now - seconds) * 10**9)
        return Timestamp(seconds=seconds, nanos=nanos)

    def parse_timestamp(self, timestamp: Timestamp) -> float:
        return timestamp.seconds + (timestamp.nanos / 10**9)

    def send_message_receive_message(self, msg: str) -> Tuple[int, str, str]:
        pb_message = example_pb2.SimpleExampleMessage(
            id=self.message_id, timestamp=self.create_timestamp(), message=msg)

        try:
            pb_response = self.stub.MessageToMessageExample(pb_message)
        except grpc.RpcError as rpc_error:
            if rpc_error.code() == grpc.StatusCode.UNAVAILABLE:
                raise RuntimeError('Cannot connect to server, make sure it\'s running!') from rpc_error
            else:
                raise rpc_error

        self.message_id += 1
        return (pb_response.id, self.parse_timestamp(pb_response.timestamp), pb_response.message)

