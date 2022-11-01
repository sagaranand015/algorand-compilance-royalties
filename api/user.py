import json
from flask import jsonify, request
from http import HTTPStatus

from .auth import encode_user_token
from utils.constants import AUTH_FILE


def new_user_registration():
    """
    Givenn the address, returns an API key/token containing the user address and some randomness.
    Uses a JWT token behind the scenes.
    """
    try:
        req = request.get_json()
        user_address = req.get("user_address")
        if not user_address:
            return (
                jsonify(
                    dict(
                        status=False,
                        message="Invalid Request Body. Pass user_address",
                    )
                ),
                HTTPStatus.BAD_REQUEST,
            )

        jwt_token = encode_user_token(user_address)
        with open(AUTH_FILE, "r") as fp:
            auth_dict = json.loads(fp.read())
            auth_dict[user_address] = jwt_token

        with open(AUTH_FILE, "w") as fp:
            fp.write(json.dumps(auth_dict))

        return (
            jsonify(
                dict(
                    status=True,
                    message="Success",
                    user_address=user_address,
                    token=jwt_token,
                )
            ),
            HTTPStatus.OK,
        )
    except Exception as e:
        print("NEW USER REGISTRATION FAILED: ", e)
        return jsonify(dict(status=False)), HTTPStatus.INTERNAL_SERVER_ERROR
