# Install for yourself: pip install grpcio-tools
python -m grpc_tools.protoc -I./protos --python_out=./src --pyi_out=./src --grpc_python_out=./src ./protos/profiles.proto

# Copy to backend service:
cp src/profiles_pb2* ../backend/src