# -------- Imports --------
import asyncio
import websockets
import json
import random
from websockets.exceptions import ConnectionClosedError
from urllib.parse import urlencode
from .logging import logger

# -------- Websocket Class --------
class Websocket():
    # -- Setup websocket variables
    def __init__(self):
        self.endpoints = [
            "wss://jetstream1.us-east.bsky.network/subscribe",
            "wss://jetstream2.us-east.bsky.network/subscribe",
            "wss://jetstream1.us-west.bsky.network/subscribe",
            "wss://jetstream2.us-west.bsky.network/subscribe"
        ]
        self.wanted_collections = urlencode([
            ("wantedCollections", "app.bsky.feed.post"),
            ("wantedCollections", "app.bsky.graph.follow")
        ])

        self.current_endpoint = 0

        self.reconnect = 1
        self.connected = False
        self.ws = None
        self.stop_event = asyncio.Event()

        self.disconnect_count = 0
        self.reconnect_count = 0
        self.total_connected_time = 0
        self.last_connected_at = None

        self.queue_status = {}

    # -------------
    # -- Connect function
    async def connect(self, queues: list) -> None:
        self.connected = True
        self.stop_event.clear()

        # -- Try to connect infinitely 
        while self.connected:
            connected_at = None
            if self.current_endpoint >= len(self.endpoints):
                random.shuffle(self.endpoints)
                self.current_endpoint = 0

            try:
                endpoint = self.endpoints[self.current_endpoint]
                logger.info(f"[Jetstream] Attempting to connect to {endpoint}...")
                async with websockets.connect(f"{endpoint}?{self.wanted_collections}", ping_interval=20, ping_timeout=40, open_timeout=20, close_timeout=10) as ws:
                    logger.info(f"[Jetstream] Connected to {endpoint}")
                    self.ws = ws
                    connected_at = asyncio.get_running_loop().time()

                    # -- Get new messages and add them to the queues
                    async for raw_message in ws:
                        try:
                            message = json.loads(raw_message)

                            # -- Add the message to each queue
                            for i, queue in enumerate(queues):
                                status = self.queue_status.setdefault(i, {
                                    "full": False,
                                    "near_capacity": False
                                })

                                qsize = queue.qsize()
                                maxsize = queue.maxsize

                                # -- Report the queue as full
                                if queue.full():
                                    if not status["full"]:
                                        logger.warning(f"[Jetstream] Queue {i} is full ({qsize}/{maxsize})")

                                    status["full"] = True
                                    status["near_capacity"] = False
                                    continue

                                # -- Reset status once the queue has room again
                                status["full"] = False

                                # -- Report the queue as nearing capacity
                                if maxsize > 0 and qsize >= maxsize * 0.8:
                                    if not status["near_capacity"]:
                                        logger.warning(f"[Jetstream] Queue {i} nearing capacity ({qsize}/{maxsize})")

                                    status["near_capacity"] = True
                                else:
                                    status["near_capacity"] = False

                                queue.put_nowait(message)

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
                self.current_endpoint += 1

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