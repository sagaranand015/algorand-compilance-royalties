import jwt
import typing
import os
import json

from utils.constants import AUTH_FILE, REGULATOR_FILE, BUSINESS_FILE


def get_address_from_decoded_token(decoded_token: typing.Dict):
    return decoded_token["sub"]


def get_server_secret_key():
    sec_key = os.getenv("SERVER_SECRET_KEY")
    if sec_key is None:
        print("DEFINE SECRET KEY FOR THE SERVER API")
        raise Exception("No Secret Key Defined for the API. ")
    return sec_key


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


def check_api_authorization(
    auth_header: str,
) -> typing.Tuple[bool, typing.Optional[typing.Dict]]:
    """
    Validates the token and returns the decoded token if validation is success
    """
    if not auth_header:
        return False, None

    if bearer_header := auth_header.split(" "):
        if bearer_header[0] != "Bearer":
            return False, None

    auth_token = bearer_header[1]
    (validated, decoded_token) = validate_user_token(auth_token)
    if not validated:
        return False, None

    print("========== decoded token is: ", decoded_token)
    return True, decoded_token


def get_regulator_data_from_storage(
    regulator_address: str,
) -> typing.Optional[typing.List[typing.Dict]]:
    """
    Returns all the data stored for the regulator address.
    Returns null if the regulator entry is not there
    """
    with open(REGULATOR_FILE, "r") as fp:
        all_data = json.load(fp)

    return all_data.get(regulator_address)


def get_business_data_from_storage(
    biz_address: str,
) -> typing.Optional[typing.Dict]:
    """
    Returns all the data stored for the business address.
    Returns null if the business entry is not there
    """
    with open(BUSINESS_FILE, "r") as fp:
        all_data = json.load(fp)

    return all_data.get(biz_address)


def get_all_regulator_data() -> typing.Dict:
    """
    Returns all the regulator data from the regulator file
    """
    with open(REGULATOR_FILE, "r") as fp:
        all_data = json.load(fp)
    return all_data


def update_regulator_data_in_storage(
    regulator_address: str, data: typing.Dict, new_data: bool = False
):
    """
    Updates or Adds the data given for the regulator address in the storage file
    """
    all_data = get_all_regulator_data()
    reg_data = all_data.get(regulator_address)
    print("========= reg_data in utils is: ", reg_data)
    if reg_data is None:
        all_data[regulator_address] = [data]
    else:
        if new_data:
            reg_data.append(data)
            all_data[regulator_address] = reg_data
        else:
            new_data = []
            for reg_d in reg_data:
                if reg_d["app_id"] == data["app_id"]:
                    new_data.append(data)
                else:
                    new_data.append(reg_d)
            all_data[regulator_address] = new_data

    print("==== final all_data is: ", all_data)
    # print("==== final reg_data, new_data is: ", reg_data, new_data)
    with open(REGULATOR_FILE, "w") as fp:
        json.dump(all_data, fp)


def get_all_business_data() -> typing.Dict:
    """
    Returns all the business data from the regulator file
    """
    with open(BUSINESS_FILE, "r") as fp:
        all_data = json.load(fp)
    return all_data


def update_business_data_in_storage(biz_address: str, data: typing.Dict):
    """
    Updates or Adds the data given for the business address in the storage file
    """
    all_data = get_all_business_data()
    all_data[biz_address] = data
    with open(BUSINESS_FILE, "w") as fp:
        json.dump(all_data, fp)
