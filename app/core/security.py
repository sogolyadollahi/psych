from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash 

from app.core.config import settings

PasswordHash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)