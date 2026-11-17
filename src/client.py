# -------- Imports --------
from atproto import Client
import httpx
from .definitions import AuthenticationError, RateLimitedError, NetworkError, UnknownError, APIError
from .logging import logger

# -------- Login Function --------
async def login(did: str, password: str) -> Client:
    try:
        # -- Setup client connection
        client = Client()

        profile = client.login(did, password)
        client.profile = profile
        logger.info(f"[Client] Logged in as {profile.handle}")
        return client # Return both the client and profile objects
    except Exception as e:
        if hasattr(e, "response") and hasattr(e.response, "status_code"):
            code = e.response.status_code
            if code == 401:
                raise AuthenticationError("[Client] Invalid account DID or password.")
            elif code in [500, 501, 502, 503, 504]:
                raise NetworkError("[Client] A network error has occured.")
            elif code == 429:
                raise RateLimitedError("[Client] Account is currently being rate limited.")
            else:
                raise APIError(f"[Client] Unhandled API error (Status {code}): {e}")
        elif isinstance(e, httpx.RequestError):
            raise NetworkError(f"[Client] Network error occurred: {e}")
        else:
            raise UnknownError(f"[Client] Unexpected error occurred: {e}")