# Install for yourself: pip install grpcio-tools
python -m grpc_tools.protoc -I./protos --python_out=./src/grpc_files --pyi_out=./src/grpc_files --grpc_python_out=./src/grpc_files ./protos/profiles.proto

sed -i 's/import profiles_pb2 as profiles__pb2/from . import profiles_pb2 as profiles__pb2/g' src/grpc_files/profiles_pb2_grpc.py

# Copy to backend service:
cp src/grpc_files/profiles_pb2* ../backend/src/grpc_files
