NUM_WORKERS=3
TIMEOUT=120

if [ "$RUN_MODE" = "ASYNC" ]
then
  python profiles_server_async.py
else
  python profiles_server.py
fi