NUM_WORKERS=3
TIMEOUT=120

if [ "$RUN_MODE" = "GRPC" ]
then
  python profiles_server_grpc.py
else
  python profiles_server.py
fi