# Install for yourself: pip install grpcio-tools
python -m grpc_tools.protoc -I./protos --python_out=./src/grpc --pyi_out=./src/grpc --grpc_python_out=./src/grpc ./protos/profiles.proto