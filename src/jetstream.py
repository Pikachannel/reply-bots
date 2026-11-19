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
        self.stop_event = asyncio.Event()

        self.disconnect_count = 0
        self.reconnect_count = 0
        self.total_connected_time = 0
        self.last_connected_at = None

    # -------------
    # -- Connect function
    async def connect(self, queues: list) -> None:
        self.connected = True
        self.stop_event.clear()

        # -- Try to connect infinitely 
        while self.connected:
            connected_at = None
            try:
                async with websockets.connect(self.endpoint, ping_interval=20, ping_timeout=40) as ws:
                    logger.info(f"[Jetstream] Connected to {self.endpoint}")
                    self.ws = ws
                    connected_at = asyncio.get_running_loop().time()

                    # -- Get new messages and add them to the queues
                    async for raw_message in ws:
                        try:
                            message = json.loads(raw_message)

                            for queue in queues:
                                await queue.put(message)
                        except json.JSONDecodeError:
                            continue

            except ConnectionClosedError as e:
                logger.warning(f"[Jetstream] Connection lost ({e})")

            except Exception as e:
                logger.error(f"[Jetstream] Connection error: {type(e).__name__} {e}")

            finally:
                if connected_at is not None:
                    connected_for = asyncio.get_running_loop().time() - connected_at

                    self.total_connected_time += connected_for
                    self.disconnect_count += 1

                    logger.info(
                        f"[Jetstream] Connection duration: {connected_for:.1f}s | "
                        f"Disconnects: {self.disconnect_count} | "
                        f"Total uptime: {self.total_connected_time:.1f}s"
                    )

                    if connected_for >= 30:
                        self.reconnect = 1

                self.ws = None

            if self.connected:
                self.reconnect_count += 1

                logger.info(f"[Jetstream] Reconnecting in {self.reconnect}s (attempt {self.reconnect_count})")

                if not await self.wait_reconnect():
                    break
                
    # -------------
    # -- Reconnect function
    async def wait_reconnect(self) -> bool:
        try:
            await asyncio.wait_for(self.stop_event.wait(), timeout=self.reconnect)
            return False
        except asyncio.TimeoutError:
            self.reconnect = min(self.reconnect * 2, 60)
            return True
      
    # -------------
    # -- Disconnect function
    async def disconnect(self) -> None:
        self.connected = False
        self.stop_event.set()

        if self.ws:
            await self.ws.close()
            logger.info("[Jetstream] Disconnected.")