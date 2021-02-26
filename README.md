# gRPC-PySide6-Example

gRPC + PySide6 example project (Qt client + non-Qt server).
Tested using Python 3.9 on Windows 10. Should work on any OS and Python version that supports gRPC and PySide6.

## Prerequisites

gRPC and PySide6 installed, either via pip or in virtualenv.

```bash
python -m pip install grpcio-tools PySide6
```

## Running

First, run `main_server.py` with at least port, default IP is `127.0.0.1`.

```bash
python ./main_server.py 8080
```

or, if you want to specify IP:

```bash
python ./main_server.py --ip 127.1.2.3 8080
```

And then, run the client. Enter the IP address and port in GUI, and try to send some data.
The debug output will be present in console.

## Misc

If you want to change and re-generate the protocols, just run `generate_grpc.sh` (under Linux) or `generate_grpc.bat` (under Windows).
**You also HAVE TO modify the import in `ExampleService_pb2_grpc.py` file, because of the project structure.**

Change

```python
import ExampleService_pb2 as ExampleService__pb2
```

to

```python
import proto.ExampleService_pb2 as ExampleService__pb2
```

at the top of the file.
