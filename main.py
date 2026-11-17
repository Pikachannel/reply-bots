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
passwords = []
account_dids = []
bots = {}
followers_set = {}
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
    global passwords
    global account_dids

    account_configs = {}

    # -- Discover configured accounts
    for key, value in os.environ.items():
        if key.startswith("ACCOUNT_DID_"):
            account_number = key.removeprefix("ACCOUNT_DID_")

            if not account_number.isdigit() or int(account_number) < 1:
                raise ConfigError(
                    "[Main] Configured accounts must use positive integers."
                )

            account_number = int(account_number)

            if account_number in account_configs:
                raise ConfigError(
                    f"[Main] Duplicate account number: {account_number}."
                )

            account_configs[account_number] = value.strip()

    # -- Validate account numbering
    if not account_configs:
        raise ConfigError("[Main] No accounts configured.")

    expected_numbers = set(range(1, len(account_configs) + 1))

    if set(account_configs) != expected_numbers:
        raise ConfigError("[Main] Gap detected in configured accounts.")

    # -- Load accounts in numerical order
    for account_number in sorted(account_configs):
        did = account_configs[account_number]
        password = os.getenv(f"PASSWORD_{account_number}", "").strip()

        if not did:
            raise ConfigError(f"[Main] ACCOUNT_DID_{account_number} is missing.")

        if not password:
            raise ConfigError(f"[Main] PASSWORD_{account_number} is missing.")

        if did in account_dids:
            raise ConfigError("[Main] Duplicate account DIDs found.")

        account_dids.append(did)
        passwords.append(password)

        bots[did] = {}
        followers_set[did] = set()

    # -- Setup Word of the Day
    if word_bot:
        try:
            word_bot_num = int(word_bot)
        except ValueError:
            raise ConfigError("[Main] WORD_OF_THE_DAY_BOT must be a valid account number.")

        if not 1 <= word_bot_num <= len(account_dids):
            raise ConfigError("[Main] WORD_OF_THE_DAY_BOT must refer to a configured account number.")

        word_bot_did = account_dids[word_bot_num - 1]

# -------- Main Functions --------
async def run() -> None:
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

async def main() -> None:
    try:
        validate_logs()
        setup_logger()
        validate_config()
        await run()
    except (ConfigError, AuthenticationError, NetworkError, APIError, RateLimitedError, UnknownError) as e:
        logger.critical(f"{e}")

if __name__ == "__main__":
    asyncio.run(main())
    