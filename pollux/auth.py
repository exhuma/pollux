"""
Module dealing with authentication of users
"""

import logging
from datetime import datetime, timedelta
from enum import Enum
from json import load
from typing import Any, Dict, Set

import bcrypt
import jwt
from jwt.exceptions import InvalidTokenError  # type: ignore

LOG = logging.getLogger(__name__)


class Permission(str, Enum):

    UPLOAD_DATA = "upload_data"


def auth(username: str, password: str, authfile: str) -> Set[Permission]:
    """
    Authenticate a user and return the permissions for that user
    """
    with open(authfile) as fptr:
        data = load(fptr)
    if username not in data:
        return set()

    hashed_pw = data[username]["password"]
    if bcrypt.checkpw(password.encode("utf8"), bytes.fromhex(hashed_pw)):
        return {Permission(perm) for perm in data[username]["permissions"]}

    return set()

def hash_pw(plain: str) -> str:
    hashed = bcrypt.hashpw(plain.encode("utf8"), bcrypt.gensalt())
    return hashed.hex()


def encode_jwt(jwt_body: Dict[str, Any], secret: str) -> str:
    expires_at = datetime.utcnow() + timedelta(days=3)
    token = jwt.encode({**jwt_body, "exp": expires_at}, secret, algorithm="HS256")
    return token.decode("ascii")


def decode_jwt(token: str, secret: str) -> Dict[str, Any]:
    try:
        auth_info = jwt.decode(token, secret, algorithm="HS256")
    except InvalidTokenError:
        LOG.debug("Unable to decode the JWT token", exc_info=True)
        return {}
    return auth_info


def refresh_token(token: str, secret: str) -> str:
    auth_info = decode_jwt(token, secret)
    auth_info.pop("exp", "")
    if not auth_info:
        return ""
    output = encode_jwt(auth_info, secret)
    return output