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
import asyncio
import os
import json
from dotenv import load_dotenv

# -------- Variables --------
load_dotenv()

# -- Account info
get_bot_num = 1
handles = []
passwords = []
account_dids = []
bots = {}
followers_set = {}

while os.getenv(f"HANDLE_{get_bot_num}"):
    handles.append(os.getenv(f"HANDLE_{get_bot_num}"))
    passwords.append(os.getenv(f"PASSWORD_{get_bot_num}"))
    account_dids.append(os.getenv(f"ACCOUNT_DID_{get_bot_num}"))
    bots[account_dids[-1]] = {
        "handle": handles[-1]
    }
    followers_set[account_dids[-1]] = set()

    get_bot_num += 1

# -- File paths
MESSAGES_JSON_PATH = "data/messages.json"
USER_DATA_PATH = "data/user_data.json"
BLOCKLIST_PATH = "data/blocklist.txt"

# -------- Load json files --------
with open(MESSAGES_JSON_PATH, "r", encoding="utf-8") as f:
    messages = json.load(f)

with open(USER_DATA_PATH, "r", encoding="utf-8") as f:
    user_data = json.load(f)

with open(BLOCKLIST_PATH, "r") as f:
    keyword_list = {line.strip().lower() for line in f}


# ------ Main Function --------
async def main() -> None:
    # -- Setup client connection
    queues = []

    for i in range(len(account_dids)):
        client = await login(handles[i], passwords[i])
        if not client:
            input("[Main] Press enter to exit...")
            return
        bots[account_dids[i]]["client"] = client

    # -- Create queues
    json_queue = asyncio.Queue(maxsize=50)

    # -- Setup classes
    ws = Websocket()
    command_manager = CommandManager(user_data, json_queue)
    dm_worker = DmWorker(bots, command_manager, json_queue, account_dids)

    filters = Filters(bots[account_dids[0]]["client"], keyword_list)

    post_manager = PostManager(bots, user_data, account_dids, messages, filters)

    # -- Start global workers
    asyncio.create_task(dm_worker.start())
    asyncio.create_task(json_worker(USER_DATA_PATH, json_queue, user_data))
    asyncio.create_task(word_of_the_day(bots[account_dids[1]]["client"], keyword_list))  # Assuming you want to use the first bot for posting the word of the day

    # -- Start per bot queues and workers
    for i in range(len(account_dids)):
        queues.append(asyncio.Queue(maxsize=300))
        asyncio.create_task(refresh_followers(bots[account_dids[i]]["client"], followers_set[account_dids[i]], account_dids[i]))
        asyncio.create_task(worker(bots[account_dids[i]]["client"], queues[i], followers_set[account_dids[i]], account_dids[i], messages, user_data, post_manager))

    # -- Setup websocket connection to the bsky jetstream
    await ws.connect(queues)
