# -------- Imports --------
import asyncio
from atproto import Client
from .logging import logger

# -------- Refresh Followers Function --------
async def refresh_followers(client: Client, followers_set: set, account_did: str, per_page: int = 100) -> None:
    # -- Start function
    while True:
        try:
            all_followers = []
            cursor = None

            # -- Loop through all pages
            while True:
                params = {"actor": account_did, "limit": per_page}
                if cursor:
                    params["cursor"] = cursor

                # -- Get the followers page
                response = await asyncio.to_thread(client.app.bsky.graph.get_followers,params=params)
                followers_page = response.followers

                all_followers.extend(followers_page) # Add new followers to the list

                # -- Get the cursor
                next_cursor = getattr(response, "cursor", None)
                if callable(next_cursor):
                    next_cursor = next_cursor()

                if not next_cursor:
                    break # Stop if it's on the last page
                cursor = next_cursor

            # -- Extract all user DIDs and add them to the set
            follower_dids = [f.did for f in all_followers]

            followers_set.clear()      
            followers_set.update(follower_dids)  
            logger.info(f"[Follower Refresh] {len(followers_set)} followers loaded for {client.profile.handle}")
        except Exception as e:
            logger.error(f"[Follower Refresh] Error updating follower list: {type(e).__name__} {e}")
        await asyncio.sleep(300) # Get followers every 5 minutes
