# Install for yourself: pip install grpcio-tools
python -m grpc_tools.protoc -I./protos --python_out=./src --pyi_out=./src --grpc_python_out=./src ./protos/profiles.proto