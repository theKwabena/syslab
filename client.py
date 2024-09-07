# ws_client.py
import asyncio
import websockets


async def send_command(command):
    uri = "ws://127.0.0.1:8000/ws"

    async with websockets.connect(uri) as websocket:
        # Send the command to the WebSocket server
        await websocket.send(command)
        print(f"Sent: {command}")
        response = await websocket.recv()
        print(f"Received: {response}")


async def main():
    while True:
        command = input("Enter command to run in Docker container: ")
        if command.lower() == "exit":
            break
        await send_command(command)


if __name__ == "__main__":
    asyncio.run(main())
