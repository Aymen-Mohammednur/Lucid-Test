from pathlib import Path
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os
from functools import lru_cache

@lru_cache
def settings():
    """Return cached configuration pulled from the environment."""
    return {
        "SECRET_KEY": os.getenv("SECRET_KEY"),
        "ALGORITHM": "HS256",
        "ACCESS_TOKEN_EXPIRE_MINUTES": int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")),
        "DATABASE_URL": os.getenv("DATABASE_URL"),
    }

# Convenient direct attributes
_SECRET = settings()
SECRET_KEY = _SECRET["SECRET_KEY"]
ALGORITHM = _SECRET["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = _SECRET["ACCESS_TOKEN_EXPIRE_MINUTES"]
DATABASE_URL = _SECRET["DATABASE_URL"]
