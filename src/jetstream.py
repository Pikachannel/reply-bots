# -------- Imports --------
import asyncio
import websockets
import json
from websockets.exceptions import ConnectionClosedError
from .logging import logger

# -------- Websocket Class --------
class Websocket():
    # -- Setup websocket variables
    def __init__(self):
        self.endpoint = "wss://jetstream1.us-east.bsky.network/subscribe"
        self.reconnect = 1
        self.connected = False
        self.ws = None

    # -------------
    # -- Connect function
    async def connect(self, queues: list) -> None:
        # Try to connect infinitely 
        self.connected = True
        while self.connected:
            try:
                # Connect to the bsky jetstream
                async with websockets.connect(self.endpoint) as ws:
                    logger.info(f"[Jetstream] Connected to {self.endpoint}")
                    self.reconnect = 1
                    self.ws = ws

                    async for raw_message in ws: # Get new messages
                        try:
                            message = json.loads(raw_message)

                            # Add them to a queue for the worker function
                            for queue in queues:
                                await queue.put(message)
                        except json.JSONDecodeError:
                            continue
            except ConnectionClosedError as e:
                logger.warning(f"[Jetstream] Connection lost ({e}); reconnecting in {self.reconnect} seconds")
                await asyncio.sleep(self.reconnect) # Wait to connect upon disconnection 
                self.reconnect = min(self.reconnect * 2, 60)

            except Exception as e:
                logger.error(f"[Jetstream] Connection error ({e}); reconnecting in {self.reconnect} seconds")
                await asyncio.sleep(self.reconnect) # Wait to reconnect upon error
                self.reconnect = min(self.reconnect * 2, 60)
                
    # -------------
    # -- Disconnect function
    async def disconnect(self) -> None:
        self.connected = False

        if self.ws:
            await self.ws.close() # Disconnect if connection is open
            logger.info("[Jetstream] Disconnected.")