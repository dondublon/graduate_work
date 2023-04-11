import asyncio
import logging

import grpc


from fastapi import FastAPI, Depends

from config import settings
from grpc_files import profiles_pb2_grpc
from profiles_server import Profiles

app = FastAPI(dependencies=[Depends(Profiles)])


async def serve() -> None:
    server = grpc.aio.server()

    profiles_pb2_grpc.add_ProfilesServicer_to_server(Profiles(), server)

    server.add_insecure_port(f'[::]:{settings.service_port}')
    logging.info(f"Starting server on %s', '[::]:{settings.service_port}")
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
