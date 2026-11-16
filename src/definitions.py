# ---- Stop Flag ----
class Stop:
    pass
STOP = Stop()

# ---- Config Error ----
class ConfigError(Exception):
    pass

# ---- Authentication Error ----
class AuthenticationError(Exception):
    pass

# ---- Network Error ----
class NetworkError(Exception):
    pass

# ---- Rate Limited Error ----
class RateLimitedError(Exception):
    pass

# ---- Unknown Error ----
class UnknownError(Exception):
    pass