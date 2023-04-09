# Install for yourself: pip install grpcio-tools
python -m grpc_tools.protoc -I./protos --python_out=./src/grpc_files --pyi_out=./src/grpc_files --grpc_python_out=./src/grpc_files ./protos/profiles.proto

# Copy to backend service:
cp src/grpc_files/profiles_pb2* ../backend/src/grpc_files

#!!! Edit file manually profiles/src/grpc_files/profiles_pb2_grpc.py and backend/src/grpc_files/profiles_pb2_grpc.py:
# import users_pb2 as users__pb2` ---> `from . import users_pb2 as users__pb2