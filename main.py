# -------- Imports --------
from src.jetstream import Websocket
from src.followers import refresh_followers
from src.worker import worker
from src.dm_worker import DmWorker
from src.settings import CommandManager
from src.post import PostManager
from src.filters import Filters
from src.client import login
from src.json_worker import json_worker
from src.word import word_of_the_day
from src.tone import ToneAnalysis
from src.shutdown import shutdown_signals
import asyncio
import os
import json
from dotenv import load_dotenv
from pathlib import Path

# -------- Variables --------
load_dotenv()

# -- Account info
get_bot_num = 1
passwords = []
account_dids = []
bots = {}
followers_set = {}

while os.getenv(f"ACCOUNT_DID_{get_bot_num}"):
    passwords.append(os.getenv(f"PASSWORD_{get_bot_num}"))
    account_dids.append(os.getenv(f"ACCOUNT_DID_{get_bot_num}"))
    bots[account_dids[-1]] = {}
    followers_set[account_dids[-1]] = set()

    get_bot_num += 1

# -- Validate account configuration
if not passwords or not account_dids or len(passwords) != len(account_dids):
    raise ValueError("[Main] Invalid account configuration.")

for i, password in enumerate(passwords, start=1):
    if not password:
        raise ValueError(f"[Main] PASSWORD_{i} is missing.")

# -- File paths
BASE_DIR = Path(__file__).resolve().parent
MESSAGES_JSON_PATH = BASE_DIR / "data" / "messages.json"
USER_DATA_PATH = BASE_DIR / "data" / "user_data.json"
BLOCKLIST_PATH = BASE_DIR / "data" / "blocklist.txt"
LOCALES_PATH = BASE_DIR / "data" / "locales.json"

# -------- Load json files --------
with open(MESSAGES_JSON_PATH, "r", encoding="utf-8") as f:
    messages = json.load(f)

with open(USER_DATA_PATH, "r", encoding="utf-8") as f:
    user_data = json.load(f)

with open(BLOCKLIST_PATH, "r") as f:
    keyword_list = {line.strip().lower() for line in f}

with open(LOCALES_PATH, "r", encoding="utf-8") as f:
    setting_replies = json.load(f)

# ------ Main Function --------
async def main() -> None:
    # -- Setup shutdown signals
    stop_event = asyncio.Event()
    shutdown_signals(stop_event)

    # -- Initialize resources
    queues = []
    workers = []

    ws, websocket_task, dm_worker, dm_task, json_queue, json_task = None, None, None, None, None, None

    # -- Setup client connection
    for i in range(len(account_dids)):
        if stop_event.is_set():
            return

        client = await login(account_dids[i], passwords[i])
        if not client:
            input("[Main] Press enter to exit...")
            return

        bots[account_dids[i]]["client"] = client
        bots[account_dids[i]]["handle"] = client.profile.handle
    if stop_event.is_set():
        return

    try:
        # -- Create queues
        json_queue = asyncio.Queue(maxsize=50)

        # -- Setup classes
        ws = Websocket()
        command_manager = CommandManager(user_data, json_queue, setting_replies)
        dm_worker = DmWorker(bots, command_manager, account_dids)
        tone_analysis = ToneAnalysis(keyword_list)

        filters = Filters(bots[account_dids[0]]["client"], tone_analysis)

        post_manager = PostManager(bots, user_data, account_dids, messages, filters)

        # -- Start global workers
        dm_task = asyncio.create_task(dm_worker.start())
        json_task = asyncio.create_task(json_worker(str(USER_DATA_PATH), json_queue, user_data))

        # -- Setup Word of the Day
        word_bot = os.getenv("WORD_OF_THE_DAY_BOT", "").strip()

        if word_bot:
            try:
                # -- Validate bot number
                word_bot_num = int(word_bot)
                if word_bot_num < 1 or word_bot_num > len(account_dids):
                    raise ValueError

                word_bot_did = account_dids[word_bot_num - 1]
                workers.append(asyncio.create_task(word_of_the_day(bots[word_bot_did]["client"], keyword_list)))
            except ValueError:
                raise ValueError("[Main] WORD_OF_THE_DAY_BOT must refer to a configured account number.")

        # -- Start per bot queues and workers
        for i in range(len(account_dids)):
            queues.append(asyncio.Queue(maxsize=300))
            workers.append(asyncio.create_task(refresh_followers(bots[account_dids[i]]["client"], followers_set[account_dids[i]], account_dids[i])))
            workers.append(asyncio.create_task(worker(bots[account_dids[i]]["client"], queues[i], followers_set[account_dids[i]], account_dids[i], messages, user_data, post_manager)))

        # -- Setup websocket connection to the bsky jetstream
        websocket_task = asyncio.create_task(ws.connect(queues))

        await stop_event.wait()

    finally:
        # -- End tasks
        print("[Main] Shutting down...")

        # -- Stop Jetstream connection
        if ws:
            await ws.disconnect()

        if websocket_task:
            websocket_task.cancel()
            await asyncio.gather(websocket_task, return_exceptions=True)

        # -- Stop workers
        print("[Main] Stopping workers...")

        for task in workers:
            task.cancel()

        print("[Main] Stopped all workers.")

        if workers:
            await asyncio.gather(*workers, return_exceptions=True)

        # -- Stop DM Worker
        if dm_worker:
            await dm_worker.stop()

        if dm_task:
            await asyncio.gather(dm_task, return_exceptions=True)

        # -- Finish pending JSON updates
        if json_queue and json_task:
            print(f"[Main] Waiting for JSON queue ({json_queue.qsize()} items)...")
            await json_queue.join()

            print("[Main] JSON queue finished.")

            # -- Stop JSON worker
            await json_queue.put("Stop")
            await json_task

            print("[Main] JSON worker stopped.")

        print("[Main] Shutdown complete.")

if __name__ == "__main__":
    asyncio.run(main())
