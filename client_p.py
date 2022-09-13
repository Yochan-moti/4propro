import asyncio
import websockets

async def hello():
    uri = "ws://127.0.0.1:30000"
    async with websockets.connect(uri, ping_interval=None) as websocket:
        print(f"wait....")
        while True:
            greeting = await websocket.recv()
            print(f"<<< ",greeting)
            # if(greeting=="UP"):
            #     print(f"<<< UP")
            # if(greeting=="RIGHT"):
            #     print(f"<<< RIGHT")
            # if(greeting=="LEFT"):
            #     print(f"<<< LEFT")



asyncio.run(hello())
