import logging

import grpc
import uvicorn
from fastapi import FastAPI

from grpc_files import profiles_pb2, profiles_pb2_grpc
from logger import LOGGING

app = FastAPI()


@app.get(
    "/sample-register",
    description="Зарегистрировать тестового пользователя",
)
async def run_register():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    logging.info("Will try to register a user ...")
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = profiles_pb2_grpc.ProfilesStub(channel)
        try:
            response = stub.Register(
                profiles_pb2.RegisterCredentials(
                    id="beab23a8-08fa-4981-8f81-4e9c92969b45",
                    first_name="Иван",
                    family_name="Иванов",
                    father_name="Иванович",
                    email="yandex1@forever.ru",
                    phone="+79173712345",
                )
            )
            return "Client received"
        except Exception as e:
            logging.error(e)
            return "Error"


if __name__ == "__main__":
    config = uvicorn.run(  # ok
        "profiles_client_sample:app",
        host="localhost",
        port=8085,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )
