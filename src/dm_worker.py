# -------- Imports --------
from atproto import Client, models
from typing import Any
import asyncio
from datetime import datetime, timezone, timedelta

# -------- DmWorker Class --------
class DmWorker:
    def __init__(self, bots: dict, command_manager: Any, json_queue: asyncio.Queue, account_dids: list, check_interval: int = 300) -> None:
        self.bots = bots
        self.command_manager = command_manager
        self.json_queue = json_queue
        self.account_dids = account_dids
        self.check_interval = check_interval
    
    # -------------
    # -- Start the DM Worker
    async def start(self) -> None:
        print("[DM Worker] Starting DM worker")
        while True:
            try:
                await self.check_dms()
            except Exception as e:
                print(f"[DMWorker] Error: {e}")
            await asyncio.sleep(self.check_interval)
    
    # -------------
    # -- Check DMs sent to the bot
    async def check_dms(self) -> None:
        # -- Run through each bot
        for account_did in self.account_dids:
            # -- Get the messages sent to the bot
            client = self.bots[account_did]["client"]
            dm_client = client.with_bsky_chat_proxy()
            dm = dm_client.chat.bsky.convo

            convo_list = await asyncio.to_thread(dm.list_convos)
            
            # -- Loop through all users dms
            for convo in convo_list.convos:
                # -- Get last 10 messages in the conversation
                messages_response = await asyncio.to_thread(
                    dm.get_messages,
                    models.ChatBskyConvoGetMessages.Params(
                        convo_id=convo.id,
                        limit=10
                    )
                )

                messages = messages_response.messages

                # -- Find the last message sent by the bot
                last_bot_message_index = -1

                for i, message in enumerate(messages):
                    if message.sender.did == account_did:
                        last_bot_message_index = i
                        break

                # -- Only process messages after the last bot message
                if last_bot_message_index == -1:
                    unread_messages = messages
                else:
                    unread_messages = messages[:last_bot_message_index]

                # -- Process oldest messages first
                for message in reversed(unread_messages):
                    user_did = message.sender.did
                    message_text = message.text
                    sent_at = datetime.fromisoformat(
                        message.sent_at.replace("Z", "+00:00")
                    )

                    # -- Check if the message was sent in the last 5 minutes
                    now = datetime.now(timezone.utc)
                    if now - sent_at >= timedelta(minutes=5):
                        continue

                    # -- Split the message into a prefix and param
                    parts = message_text.split(maxsplit=1)
                    if not parts:
                        continue

                    command = parts[0].lower()
                    param = parts[1] if len(parts) > 1 else None

                    # -- Map to CommandManager
                    msg_to_send = None
                    facet = None

                    if command == "!nickname":
                        _, msg_to_send = await self.command_manager.update_nickname(user_did, param, account_did)
                    elif command == "!chance":
                        _, msg_to_send = await self.command_manager.chance(user_did, param, account_did)
                    elif command == "!interval":
                        _, msg_to_send = await self.command_manager.interval(user_did, param, account_did)
                    elif command == "!skip":
                        _, msg_to_send = await self.command_manager.skip_posts(user_did, param, account_did)
                    elif command == "!delete":
                        _, msg_to_send = await self.command_manager.delete_settings(user_did, param, account_did)
                    elif command == "!settings":
                        _, msg_to_send = await self.command_manager.view_settings(user_did, account_did)
                    elif command == "!sync":
                        other_dids = [did for did in self.account_dids if did != account_did]
                        _, msg_to_send = await self.command_manager.sync_settings(user_did, param, self.bots, account_did, other_dids)
                    elif command == "!language":
                        _, msg_to_send = await self.command_manager.language(user_did, param, account_did)
                    elif command == "!help":
                        _, msg_to_send, facet = await self.command_manager.help()
                    else:
                        continue

                    # -- Send response
                    if msg_to_send:
                        message_input = models.ChatBskyConvoDefs.MessageInput(
                            text=msg_to_send,
                            facets=[facet] if facet else None
                        )

                        await asyncio.to_thread(
                            dm.send_message,
                            models.ChatBskyConvoSendMessage.Data(
                                convo_id=convo.id,
                                message=message_input
                            )
                        )