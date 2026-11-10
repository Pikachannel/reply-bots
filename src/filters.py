# -------- Imports --------
import time
from typing import Any

# -------- Filters Class --------
class Filters:
    def __init__(self, client: Any, tone_analysis: Any) -> None:
        self.cache = {}
        self.client = client
        self.tone_analysis = tone_analysis

    # -------------
    # -- Check for negative sentiment
    def tone(self, message):
        text = message.get("commit", {}).get("record", {}).get("text", "").lower()
        return self.tone_analysis.get_tone(text)

    # -------------
    # -- Flag links
    def links(self, message):
        embed = message.get("commit", {}).get("record", {}).get("embed", {})
        facets = message.get("commit", {}).get("record", {}).get("facets", [])

        # -- Check for links
        has_link = any(
            feature.get("$type") == "app.bsky.richtext.facet#link"
            for facet in facets
            for feature in facet.get("features", [])
        )
        return embed.get("$type") == "app.bsky.embed.external" or has_link

    # -------------
    # -- Flag accounts with Bsky labels
    def account_flags(self, user_did: str):
        # -- Check for cached flags
        if user_did in self.cache:
            flagged, timestamp = self.cache[user_did]
            if time.time() - timestamp < 3600:
                return flagged

        # -- Check for labels
        try:
            profile =self.client.get_profile(user_did)
            labels = profile.labels or []
            
            flagged = any(label.src == "did:plc:ar7c4by46qjdydhdevvrndac" for label in labels)

            self.cache[user_did] = (flagged, time.time())
            return flagged
        except:
            return True
    
    # -------------
    # -- Flag posts with Bsky labels
    def post_flags(self, message, post_uri):
        # -- Check message for self labels
        post_labels = message.get("commit", {}).get("record", {}).get("labels", {}).get("$type", "")
        if post_labels == "com.atproto.label.defs#selfLabels":
            return True

        # -- Check for labels
        try:
            posts = self.client.app.bsky.feed.get_posts({"uris": [post_uri]})

            if not posts.posts:
                return False

            post = posts.posts[0]
            labels = post.labels or []

            flagged = len(labels) > 0
            return flagged

        except:
            return True

