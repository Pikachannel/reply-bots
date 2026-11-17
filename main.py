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
from src.definitions import STOP, ConfigError, AuthenticationError, NetworkError, UnknownError, RateLimitedError, APIError
from src.logging import logger, setup_logger, validate_logs
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

word_bot = os.getenv("WORD_OF_THE_DAY_BOT", "").strip()
word_bot_did = None

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

# -------- Validate account configuration --------
def validate_config():
    global word_bot_did

    if not passwords or not account_dids or len(passwords) != len(account_dids):
        raise ConfigError("[Main] Invalid account configuration.")

    if len(account_dids) != len(set(account_dids)):
        raise ConfigError("[Main] Duplicate account DIDs found.")

    for i, password in enumerate(passwords, start=1):
        if not password:
            raise ConfigError(f"[Main] PASSWORD_{i} is missing.")

    if word_bot:
        try:
            word_bot_num = int(word_bot)
        except ValueError:
            raise ConfigError(
                "[Main] WORD_OF_THE_DAY_BOT must be a valid account number."
            )

        if not 1 <= word_bot_num <= len(account_dids):
            raise ConfigError(
                "[Main] WORD_OF_THE_DAY_BOT must refer to a configured account number."
            )

        word_bot_did = account_dids[word_bot_num - 1]

# -------- Main Function --------
async def main() -> None:
    logger.info("[Main] Starting...")

    # -- Setup shutdown signals
    stop_event = asyncio.Event()
    shutdown_signals(stop_event)

    # -- Initialize resources
    queues = []
    workers = []

    ws, websocket_task, dm_worker, dm_task, json_queue, json_task, post_manager = None, None, None, None, None, None, None

    # -- Setup client connection
    try:
        for i in range(len(account_dids)):
            if stop_event.is_set():
                logger.error("[Main] Login failed. Shutting down...")
                return

            client = await login(account_dids[i], passwords[i])
            bots[account_dids[i]]["client"] = client
            bots[account_dids[i]]["handle"] = client.profile.handle
            
        if stop_event.is_set():
            logger.info("[Main] Shutdown requested during login.")
            return
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
        if word_bot:
            workers.append(asyncio.create_task(word_of_the_day(bots[word_bot_did]["client"], keyword_list)))

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
        logger.info("[Main] Shutting down...")

        # -- Stop Jetstream connection
        try:
            if ws:
                await ws.disconnect()
        except Exception as e:
            logger.error(f"[Main] Error disconnecting websocket: {e}")

        if websocket_task:
            websocket_task.cancel()
            await asyncio.gather(websocket_task, return_exceptions=True)

        # -- Stop workers
        for task in workers:
            task.cancel()

        if workers:
            logger.info("[Main] Stopping workers...")
            await asyncio.gather(*workers, return_exceptions=True)

            logger.info("[Main] Stopped all workers.")

        # -- Stop DM Worker
        if dm_worker:
            try:
                await dm_worker.stop()
            except Exception as e:
                logger.error(f"[Main] Error stopping DM worker: {e}")

        if dm_task:
            try:
                await asyncio.wait_for(dm_task, timeout=10)
            except asyncio.TimeoutError:
                logger.warning("[Main] DM worker timed out and was cancelled.")
            except asyncio.CancelledError:
                logger.info("[Main] DM worker was cancelled.")

            await asyncio.gather(dm_task, return_exceptions=True)

        # -- Stop profile cache cleanup
        if post_manager:
            try:
                await post_manager.cache_cleanup_stop()
            except Exception as e:
                logger.error(f"[Main] Error stopping profile cache cleanup: {e}")
   
        # -- Finish pending JSON updates
        if json_queue and json_task:
            logger.info(f"[Main] Waiting for JSON queue ({json_queue.qsize()} items)...")

            queue_empty = False

            if not json_task.done():
                try:
                    await asyncio.wait_for(json_queue.join(), timeout=30)
                    queue_empty = True
                    logger.info("[Main] JSON queue finished.")

                except asyncio.TimeoutError:
                    logger.warning("[Main] JSON queue timed out. Pending updates may be lost.")

            # -- Stop JSON worker
            if queue_empty and not json_task.done():
                try:
                    await asyncio.wait_for(json_queue.put(STOP), timeout=5)
                    await asyncio.wait_for(json_task, timeout=15)

                except asyncio.TimeoutError:
                    logger.warning("[Main] JSON worker timed out. Cancelling...")
                    json_task.cancel()
                    await asyncio.gather(json_task, return_exceptions=True)

                except Exception as e:
                    logger.error(f"[Main] JSON worker failed: {e}")
                    await asyncio.gather(json_task, return_exceptions=True)

            else:
                if not json_task.done():
                    logger.warning("[Main] JSON worker not stopped cleanly. Cancelling...")
                    json_task.cancel()

                await asyncio.gather(json_task, return_exceptions=True)

        logger.info("[Main] Shutdown complete.")

if __name__ == "__main__":
    try:
        validate_logs()
        setup_logger()
        validate_config()
        asyncio.run(main())
    except (ConfigError, AuthenticationError, NetworkError, APIError, RateLimitedError, UnknownError) as e:
        logger.critical(f"{e}")
