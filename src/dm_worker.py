# -------- Imports --------
from atproto import models
from typing import Any
import asyncio
from datetime import datetime, timezone, timedelta
from .logging import logger

# -------- DmWorker Class --------
class DmWorker:
    def __init__(self, bots: dict, command_manager: Any, account_dids: list, check_interval: int = 300) -> None:
        self.bots = bots
        self.command_manager = command_manager
        self.account_dids = account_dids
        self.check_interval = check_interval
        self.stop_event = asyncio.Event()
        self.number_of_messages = 0
    
    # -------------
    # -- Start the DM Worker
    async def start(self) -> None:
        logger.info("[DM Worker] Starting DM worker")

        while not self.stop_event.is_set():
            try:
                await self.check_dms()
            except Exception as e:
                logger.error(f"[DM Worker] Error: {e}")

            try:
                await asyncio.wait_for(self.stop_event.wait(), timeout=self.check_interval)
            except asyncio.TimeoutError:
                continue

        logger.info("[DM Worker] DM worker stopped.")

    # -------------
    # -- Stop the DM Worker
    async def stop(self) -> None:
        logger.info(f"[DM Worker] Shutting down... waiting for {self.number_of_messages} pending messages to finish.")
        self.stop_event.set()
        
    # -------------
    # -- Check DMs sent to the bot
    async def check_dms(self) -> None:
        # -- Run through each bot
        for account_did in self.account_dids:
            if self.stop_event.is_set():
                return

            try:
                client = self.bots[account_did]["client"]
                dm_client = client.with_bsky_chat_proxy()
                dm = dm_client.chat.bsky.convo

                convo_list = await asyncio.to_thread(dm.list_convos)

            except Exception as e:
                logger.error(f"[DM Worker] Error fetching conversations: {e}")
                continue

            for convo in convo_list.convos:
                if self.stop_event.is_set():
                    return

                try:
                    messages_response = await asyncio.to_thread(
                        dm.get_messages,
                        models.ChatBskyConvoGetMessages.Params(
                            convo_id=convo.id,
                            limit=10
                        )
                    )

                    messages = messages_response.messages
                    last_bot_message_index = -1
                except Exception as e:
                    logger.error(f"[DM Worker] Error fetching messages: {e}")
                    continue

                try:
                    for i, message in enumerate(messages):
                        sender = getattr(message, "sender", None)

                        if sender is not None and sender.did == account_did:
                            last_bot_message_index = i
                            break

                    # -- Only process messages after the last bot message
                    if last_bot_message_index == -1:
                        unread_messages = messages
                    else:
                        unread_messages = messages[:last_bot_message_index]

                    self.number_of_messages = len(unread_messages)

                    # -- Process oldest messages first
                    for message in reversed(unread_messages):
                        try:
                            # -- Ignore system message views
                            sender = getattr(message, "sender", None)
                            if sender is None:
                                continue

                            # -- Ignore messages with no text
                            message_text = getattr(message, "text", None)
                            if not message_text:
                                continue

                            user_did = message.sender.did

                            # -- Ignore messages sent by the bot
                            if user_did == account_did:
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
                                _, msg_to_send, facet = await self.command_manager.help(user_did, account_did)
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

                        except Exception as e:
                            logger.error(f"[DM Worker] An error occured while processing a message: {e}")
                        finally:
                            self.number_of_messages -= 1
                except Exception as e:
                    logger.error(f"[DM Worker] Unexpected conversation processing error: {e}")