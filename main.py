import docker
import asyncio
from fastapi import FastAPI, WebSocket, responses

app = FastAPI()

async def login():
    # Check user with freeipa or ad.
    # if user exists, check sqlite for container with name and id
    # check if container is running or starts it
    # if container is running, send the container id to the frontend for mount.
    # Frontend gets id and mounts it with xterm.
    pass