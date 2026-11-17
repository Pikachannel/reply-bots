# -------- Imports --------
import asyncio
import signal

# -------- Listen for shutdown signals --------
def shutdown_signals(stop_event: asyncio.Event) -> None:
    loop = asyncio.get_running_loop()

    def handle_signal(sig, frame):
        loop.call_soon_threadsafe(stop_event.set)

    signal.signal(signal.SIGINT, handle_signal)

    if hasattr(signal, "SIGTERM"):
        signal.signal(signal.SIGTERM, handle_signal)