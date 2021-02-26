import argparse
from concurrent import futures
import grpc


def main():
    arg_parser = argparse.ArgumentParser(
        description='Run gRPC server for example PySide6 + gRPC application')
    arg_parser.add_argument('--ip', type=str, dest='ip_address', default='127.0.0.1',
                            help='Server\'s IP address for listening to client connections')
    arg_parser.add_argument('port', type=int, help='Server\'s port')
    arguments = arg_parser.parse_args()

    print(f'Starting the server on {arguments.ip_address}:{arguments.port}...')


if __name__ == '__main__':
    main()
