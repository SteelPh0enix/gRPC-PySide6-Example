import argparse
import time
import grpc
import logging

from concurrent import futures
from google.protobuf.timestamp_pb2 import Timestamp

from proto import ExampleService_pb2 as example_pb2
from proto import ExampleService_pb2_grpc as example_grpc


class ExampleServicer(example_grpc.ExampleServiceServicer):
    def create_timestamp(self) -> Timestamp:
        now = time.time()
        seconds = int(now)
        nanos = int((now - seconds) * 10**9)
        return Timestamp(seconds=seconds, nanos=nanos)

    def parse_timestamp(self, timestamp: Timestamp) -> float:
        return timestamp.seconds + (timestamp.nanos / 10**9)

    def MessageToMessageExample(self, request, context):
        print(f'[message-to-message] ID: {request.id}, timestamp: {self.parse_timestamp(request.timestamp)}, message: {request.message}')
        return example_pb2.SimpleExampleResponse(id=request.id, timestamp=self.create_timestamp(), message=f'[server response] {request.message}')


def main():
    arg_parser = argparse.ArgumentParser(
        description='Run gRPC server for example PySide6 + gRPC application')
    arg_parser.add_argument('--ip', type=str, dest='ip_address', default='127.0.0.1',
                            help='Server\'s IP address for listening to client connections')
    arg_parser.add_argument('port', type=int, help='Server\'s port')
    arguments = arg_parser.parse_args()

    print(f'Starting the server on {arguments.ip_address}:{arguments.port}...')

    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    example_grpc.add_ExampleServiceServicer_to_server(
        ExampleServicer(), grpc_server)
    grpc_server.add_insecure_port(f'{arguments.ip_address}:{arguments.port}')
    grpc_server.start()
    grpc_server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    main()
