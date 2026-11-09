# -------- Imports --------
import asyncio
from datetime import datetime, timedelta, timezone
from wonderwords import RandomWord
from atproto import Client

# -------- Functions --------

# -- Post a random word --
async def post_random_word(client, blocked_words):
    # -- Get a random word
    r = RandomWord()
    word = None
    candidate = None

    # -- Have 10 attempts at finding a word
    for _ in range(10):
        candidate = r.word()
        if candidate.lower() not in blocked_words:
            word = candidate
            break
    if not word:
        return
    
    # -- Make the post
    await asyncio.to_thread(client.send_post,f"TETO WORD OF THE DAY: {word}")

# -- Already Posted --
async def already_posted(client):
    time_threshold = datetime.now(timezone.utc) - timedelta(hours=24)

    try:
        response = await asyncio.to_thread(
            client.app.bsky.feed.get_author_feed,
            actor=client.me.handle,
            limit=5,
            filter="posts_no_replies"
        )

        for feed_view in response.feed:
            post = feed_view.post

            text = post.record.text
            post_time = datetime.fromisoformat(
                post.record.created_at.replace("Z", "+00:00")
            )

            if "WORD OF THE DAY" in text.upper() and post_time >= time_threshold:
                return True

        return False

    except Exception as e:
        print(f"[Word] Failed to check recent posts: {e}")
        return None
    

# -- Post a word of the day every day
async def word_of_the_day(client, blocked_words):
    while True:
        try:
            already_posted_recently = await already_posted(client)

            # -- Post if no post has been made recently
            if already_posted_recently is False:
                await post_random_word(client, blocked_words)

        except Exception as e:
            print(f"[Word] Unexpected error: {e}")

        # -- Check again in an hour
        await asyncio.sleep(3600)
