# Install for yourself: pip install grpcio-tools
python -m grpc_tools.protoc -I./protos --python_out=./src/grpc_ --pyi_out=./src/grpc_ --grpc_python_out=./src/grpc_ ./protos/profiles.proto