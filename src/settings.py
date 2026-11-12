
# -------- Imports --------
import asyncio
from .json_worker import submit_json_update

# -------- Command Class --------
class CommandManager:
    def __init__(self, user_data: dict, json_queue: asyncio.Queue, setting_replies: dict) -> None:
        self.user_data = user_data
        self.json_queue = json_queue
        self.setting_replies = setting_replies

        self.language_map = {}

        for key in setting_replies:
            self.language_map[key.lower()] = key

            for lang, name in setting_replies[key]["language_names"].items():
                self.language_map[name.lower()] = lang



    # -------------
    # -- To float
    # Converts a string to a float
    def to_float(self, s: str) -> float | None:
        try:
            return float(s)
        except (TypeError, ValueError):
            return None

    # -------------
    # -- Get language
    # Gets a user's language setting
    def get_language(self, user_did: str, account_did: str) -> str:
        return self.user_data.get(account_did, {}).get(user_did, {}).get("lang", "en")

    # -------------
    # -- Get replies
    # Gets replies for a user's language
    def get_replies(self, user_did: str, account_did: str) -> dict:
        lang = self.get_language(user_did, account_did)
        return self.setting_replies.get(lang, self.setting_replies["en"])

    # -------------
    # -- Remove setting
    # Removes a specific setting
    async def remove_setting(self, user_did: str, setting: str, account_did: str) -> tuple[bool, str]:
        # -- Add to queue
        payload = {
            "type": "remove",
            "account_did": account_did,
            "user_did": user_did,
            "setting": setting
        }

        # -- Get replies
        replies = self.get_replies(user_did, account_did)

        success = await submit_json_update(self.json_queue, payload)
        if not success:
            return False, replies["json_error"]

        # -- Return reply
        return True, replies["remove"].format(setting=setting)

    # -------------
    # -- Nickname
    # A string at max 20 characters
    async def update_nickname(self, user_did: str, nickname: str | None, account_did: str) -> tuple[bool, str]:
        # -- Validation and normalisation
        if nickname is None:
            return await self.remove_setting(user_did, "nickname", account_did)

        nickname = nickname.strip()[:20]

        # -- Add to queue
        payload = {
            "type": "update",
            "account_did": account_did,
            "user_did": user_did,
            "nickname": nickname
        }

        # -- Get replies
        replies = self.get_replies(user_did, account_did)

        success = await submit_json_update(self.json_queue, payload)
        if not success:
            return False, replies["json_error"]

        # -- Return reply
        return True, replies["nickname"].format(nickname=nickname)

    # -------------
    # -- Chance
    # A float between 0 and 100
    async def chance(self, user_did: str, chance: str | None, account_did: str) -> tuple[bool, str]:
        # -- Validation and normalisation
        if chance is None:
            return await self.remove_setting(user_did, "chance", account_did)

        chance_value = self.to_float(chance)

        # -- Get replies
        replies = self.get_replies(user_did, account_did)

        if chance_value is None:
            return False, replies["chance_error_1"]

        if chance_value < 0 or chance_value > 100:
            return False, replies["chance_error_2"]

        chance_value = round(chance_value, 2)

        # -- Add to queue
        payload = {
            "type": "update",
            "account_did": account_did,
            "user_did": user_did,
            "chance": chance_value
        }

        success = await submit_json_update(self.json_queue, payload)
        if not success:
            return False, replies["json_error"]

        # -- Return reply
        return True, replies["chance"].format(chance_value=chance_value)

    # -------------
    # -- Interval
    # A static interval or a ranged interval
    # Between 60 and 3600 seconds
    async def interval(self, user_did: str, interval: str | None, account_did: str) -> tuple[bool, str]:
        # -- Validation and normalisation
        if interval is None:
            return await self.remove_setting(user_did, "interval", account_did)

        # -- Get replies
        replies = self.get_replies(user_did, account_did)

        # -- Check if the interval is a range or static value
        interval_split = interval.split("-")

        # -- Range
        if len(interval_split) == 2:
            interval_value_1 = self.to_float(interval_split[0])
            interval_value_2 = self.to_float(interval_split[1])

            if interval_value_1 is None or interval_value_2 is None:
                return False, replies["interval_error_1"]

            interval_format_1 = round(interval_value_1, 2)
            interval_format_2 = round(interval_value_2, 2)

            if interval_format_1 > interval_format_2:
                return False, replies["interval_error_2"]

            if interval_format_1 < 60 or interval_format_2 > 3600:
                return False, replies["interval_error_3"]

            final_value = [interval_format_1, interval_format_2]
            text_value = f"{interval_format_1}-{interval_format_2}"

        # -- Static
        else:
            interval_value = self.to_float(interval)

            if interval_value is None:
                return False, replies["interval_error_1"]

            if interval_value < 60 or interval_value > 3600:
                return False, replies["interval_error_3"]

            final_value = [round(interval_value, 2)]
            text_value = round(interval_value, 2)

        # -- Add to queue
        payload = {
            "type": "update",
            "account_did": account_did,
            "user_did": user_did,
            "interval": final_value
        }

        success = await submit_json_update(self.json_queue, payload)
        if not success:
            return False, replies["json_error"]

        # -- Return reply
        return True, replies["interval"].format(text_value=text_value)

    # -------------
    # -- Skip posts
    # A static number or ranged number of posts
    # Between 0 and 50 posts
    async def skip_posts(self, user_did: str, interval: str | None, account_did: str) -> tuple[bool, str]:
        # -- Validation and normalisation
        if interval is None:
            return await self.remove_setting(user_did, "skip", account_did)

        # -- Get replies
        replies = self.get_replies(user_did, account_did)

        # -- Check if the interval is a range or static value
        interval_split = interval.split("-")

        # -- Range
        if len(interval_split) == 2:
            interval_value_1 = self.to_float(interval_split[0])
            interval_value_2 = self.to_float(interval_split[1])

            if interval_value_1 is None or interval_value_2 is None:
                return False, replies["skip_error_1"]

            interval_format_1 = int(interval_value_1)
            interval_format_2 = int(interval_value_2)

            if interval_format_1 > interval_format_2:
                return False, replies["skip_error_2"]

            if interval_format_1 < 0 or interval_format_2 > 50:
                return False, replies["skip_error_3"]

            final_value = [interval_format_1, interval_format_2]
            text_value = f"{interval_format_1}-{interval_format_2}"

        # -- Static
        else:
            interval_value = self.to_float(interval)

            if interval_value is None:
                return False, replies["skip_error_1"]

            if interval_value < 0 or interval_value > 50:
                return False, replies["skip_error_3"]

            final_value = [int(interval_value)]
            text_value = int(interval_value)

        # -- Add to queue
        payload = {
            "type": "update",
            "account_did": account_did,
            "user_did": user_did,
            "skip": final_value
        }

        success = await submit_json_update(self.json_queue, payload)
        if not success:
            return False, replies["json_error"]
        
        # -- Return reply
        return True, replies["skip"].format(text_value=text_value)

    # -------------
    # -- Change language
    # Change the language that a bot uses
    async def language(self, user_did: str, lang: str | None, account_did: str) -> tuple[bool, str]:
        # -- Remove language setting if no value provided
        if lang is None:
            return await self.remove_setting(user_did, "lang", account_did)

        # -- Validation and normalisation
        lang = lang.strip().lower()
        lang = self.language_map.get(lang)

        # -- Get current user language & active replies dictionary
        current_lang = self.get_language(user_did, account_did)
        replies = self.get_replies(user_did, account_did)

        # -- Check if language exists
        if lang is None:
            lang_names = replies.get("language_names", {})
            available_languages = ", ".join(
                f"{lang_names.get(code, code.upper())} ({code})"
                for code in self.setting_replies
            )
            return False, replies["language_error_2"].format(
                languages=available_languages
            )

        # -- Check if already using requested language
        if lang == current_lang:
            lang_display_name = replies.get("language_names", {}).get(lang, lang.upper())
            return False, replies["language_error_1"].format(
                language=lang_display_name
            )

        # -- Add update task to queue
        payload = {
            "type": "update",
            "account_did": account_did,
            "user_did": user_did,
            "lang": lang
        }

        success = await submit_json_update(self.json_queue, payload)
        if not success:
            return False, replies["json_error"]

        # -- Get replies dictionary for the newly targeted language
        target_replies = self.setting_replies.get(lang, self.setting_replies["en"])
        target_lang_name = target_replies.get("language_names", {}).get(lang, lang.upper())

        # -- Return successful response
        return True, target_replies["language"].format(language=target_lang_name)

    # -------------
    # -- Delete
    # Deletes the user's settings
    async def delete_settings(self, user_did: str, globally: str | None, account_did: str) -> tuple[bool, str]:

        # -- Get replies
        replies = self.get_replies(user_did, account_did)

        # -- Add to queue
        payload = {
            "type": "delete",
            "user_did": user_did,
            "account_did": None if globally and globally.lower() == "all" else account_did
        }

        success = await submit_json_update(self.json_queue, payload)
        if not success:
            return False, replies["delete_error"]

        # -- Return reply
        return True, replies["delete"]

    # -------------
    # -- Settings
    # Views a user's settings
    async def view_settings(self, user_did: str, account_did: str) -> tuple[bool, str]:

        # -- Settings helper
        def format_value(key, value):
            if key == "lang":
                return replies.get("language_names", {}).get(value, value.upper())

            if isinstance(value, list):
                return f"{value[0]}-{value[1]}" if len(value) == 2 else value[0]

            return value

        # -- Get replies
        replies = self.get_replies(user_did, account_did)

        # -- Get settings
        user_settings = self.user_data.get(account_did, {}).get(user_did, {})

        if not user_settings:
            return False, replies["no_settings"]

        format_settings = "\n".join(
            f"{key.capitalize()}: {format_value(key, value)}"
            for key, value in user_settings.items()
        )

        # -- Return reply
        return True, replies["view_settings"].format(
            format_settings=format_settings
        )

    # -------------
    # -- Sync
    # Syncs a user's settings between bots
    async def sync_settings(self, user_did: str, handle: str, bots: dict, account_did: str, other_dids: list) -> tuple[bool, str]:

        # -- Get replies
        replies = self.get_replies(user_did, account_did)

        # -- Get the bot to sync with
        sync_did = None

        for did, bot in bots.items():
            if f"@{bot['handle']}" == handle:
                sync_did = did
                break

        # -- Validation
        if sync_did is None or sync_did not in bots:
            return False, replies.get(
                "sync_error",
                "An error occurred while syncing your settings.\nPlease make sure you entered a valid bot handle.\nUse !help at any time to see all commands."
            )

        # -- Get the user's settings on the sync bot
        sync_settings = self.user_data.get(sync_did, {}).get(user_did, {})

        # -- Sync the settings to the other bots
        if sync_did == account_did:

            all_successful = True
            for other_did in other_dids:
                payload = {
                    **sync_settings,
                    "type": "update",
                    "account_did": other_did,
                    "user_did": user_did
                }

                success = await submit_json_update(self.json_queue, payload)
                if not success:
                    all_successful = False

            if not all_successful:
                return False, replies["sync_error"]

            # -- Return reply after all bots are processed
            return True, replies["sync_from"].format(
                handle=bots[account_did]["handle"]
            )

        # -- Sync the settings to this bot
        else:
            payload = {
                **sync_settings,
                "type": "update",
                "account_did": account_did,
                "user_did": user_did
            }

            success = await submit_json_update(self.json_queue, payload)
            if not success:
                return False, replies["sync_error"]
            
            # -- Return reply
            return True, replies["sync_with"].format(
                handle=bots[sync_did]["handle"]
            )

    # -------------
    # -- Help
    # Sends a help message for the bot
    async def help(self, user_did: str | None = None, account_did: str | None = None) -> tuple[bool, str, dict]:

        # -- Get replies
        if user_did is not None and account_did is not None:
            lang = self.get_language(user_did, account_did)
            replies = self.get_replies(user_did, account_did)
        else:
            lang = "en"
            replies = self.setting_replies["en"]

        # -- Format help
        text = replies["help"]

        if lang == "en":
            link_text = "README"
            uri = "https://github.com/Pikachannel/reply-bots/blob/main/README.md"
        else:
            link_text = f"{lang.upper()}_README"
            uri = f"https://github.com/Pikachannel/reply-bots/blob/main/{lang.upper()}_README.md"

        byte_start = text.encode("utf-8").find(link_text.encode("utf-8"))

        # -- Create the clickable link if the text contains README file
        facet = {}

        if byte_start != -1:
            byte_end = byte_start + len(link_text.encode("utf-8"))

            facet = {
                "index": {
                    "byteStart": byte_start,
                    "byteEnd": byte_end
                },
                "features": [
                    {
                        "$type": "app.bsky.richtext.facet#link",
                        "uri": uri
                    }
                ]
            }

        # -- Return reply
        return True, text, facet
