import os
import json


def get_server_secret_key():
    sec_key = os.getenv("SERVER_SECRET_KEY")
    if sec_key is None:
        print("DEFINE SECRET KEY FOR THE SERVER API")
        raise Exception("No Secret Key Defined for the API. ")
    return sec_key
