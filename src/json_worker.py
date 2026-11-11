
# -------- Imports --------
import json
import asyncio
import os
import tempfile


# -------- Submit JSON Update --------
async def submit_json_update(queue: asyncio.Queue, update: dict) -> bool:
    # -- Create a future to receive the result
    future = asyncio.get_running_loop().create_future()

    # -- Add update and future to queue
    await queue.put({
        "update": update,
        "future": future
    })

    # -- Wait for the worker to finish
    return await future


# -------- JSON Worker Function --------
async def json_worker(path: str, queue: asyncio.Queue, user_data: dict) -> None:
    # -- Start function
    print("[JSON Worker] Worker starting")

    while True:
        item = await queue.get()
        future = item["future"]

        try:
            update = item["update"]

            account_did = update.get("account_did", "")
            user_did = update["user_did"]

            # -- Load the data from the path
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except FileNotFoundError:
                data = {}
            if account_did:
                data.setdefault(account_did, {})

            # -- Update a user's data
            if update.get("type") == "update":
                update_data = {}

                for key, value in update.items():
                    if key not in ["type", "user_did", "account_did"]:
                        update_data[key] = value

                if user_did not in data[account_did]:
                    data[account_did][user_did] = {}

                data[account_did][user_did].update(update_data)

            # -- Remove a setting
            elif update.get("type") == "remove":
                key = update["setting"]

                if user_did in data[account_did]:
                    data[account_did][user_did].pop(key, None)

            # -- Delete a user's data
            elif update.get("type") == "delete":
                if account_did:
                    if user_did in data[account_did]:
                        del data[account_did][user_did]

                else:
                    for bot_did in data:
                        data[bot_did].pop(user_did, None)

                        

            else:
                raise ValueError(f"Unknown update type: {update.get('type')}")

            # -- Write to a temporary file
            temp_path = None

            try:
                directory = os.path.dirname(os.path.abspath(path))

                with tempfile.NamedTemporaryFile(mode="w",encoding="utf-8",dir=directory,prefix=".json_tmp_",suffix=".tmp",delete=False) as f:
                    temp_path = f.name

                    json.dump(data, f, indent=4)
                    f.flush()
                    os.fsync(f.fileno())

                # -- Replace the original file
                os.replace(temp_path, path)
                temp_path = None

            finally:
                # -- Remove temporary file if writing failed
                if temp_path and os.path.exists(temp_path):
                    os.remove(temp_path)

            # -- Update in-memory data
            user_data.clear()
            user_data.update(data)

            # -- Report success
            if not future.done():
                future.set_result(True)

        except Exception as e:
            print(f"[JSON Worker] An error has occurred: {e}")

            # -- Report failure
            if not future.done():
                future.set_result(False)

        finally:
            queue.task_done()
