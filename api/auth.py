import jwt
import datetime
import json
import typing

from utils.utils import get_server_secret_key
from utils.constants import AUTH_FILE


def encode_user_token(user_address: str):
    try:
        sec_key = get_server_secret_key()
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "sub": user_address,
        }
        return jwt.encode(payload, sec_key, algorithm="HS256")
    except Exception as e:
        print("EXCEPTION IN ENCODING JWT TOKEN", e)
        raise e


def validate_user_token(
    auth_token: str,
) -> typing.Tuple[bool, typing.Optional[typing.Dict]]:
    """
    Returns true if the user token is valid and is in the list of registered tokens.
    Otherwise, returns false
    """
    if not auth_token:
        return (False, None)
    try:
        with open(AUTH_FILE) as fp:
            auth_dict = json.loads(fp.read())

        if auth_token not in auth_dict.values():
            return (False, None)

        sec_key = get_server_secret_key()
        res = jwt.decode(auth_token, sec_key, algorithms=["HS256"])
        return (True, res)
    except Exception as e:
        print("EXCEPTION IN DECODING JWT TOKEN", e)
        raise e
