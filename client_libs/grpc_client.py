from google.protobuf.timestamp_pb2 import Timestamp
from proto import ExampleService_pb2_grpc as example_grpc
from proto import ExampleService_pb2 as example_pb2
import grpc
import time


class GRPCClient():
    def __init__(self, ip, port):
        self.channel = grpc.insecure_channel(f'{ip}:{port}')
        self.stub = example_grpc.ExampleServiceStub(self.channel)

    def create_timestamp(self) -> str:
        now = time.time()
        seconds = int(now)
        nanos = int((now - seconds) * 10**9)
        return Timestamp(seconds=seconds, nanos=nanos)
