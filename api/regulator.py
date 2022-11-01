import json

from http import HTTPStatus
from flask import jsonify, request

from utils.utils import (
    check_api_authorization,
    get_address_from_decoded_token,
    get_regulator_data_from_storage,
    update_regulator_data_in_storage,
)
from utils.constants import REGULATOR_FILE

from compliance_client import ComplianceClient


def _create_get_emission_control(app_id: int = 0):
    if app_id == 0:
        return ComplianceClient()
    return ComplianceClient(app_id)


def create_emission_control():
    """
    To create an app keeping the regulator at the center and creating an emission control
    from the front end application
    """
    try:
        auth_header = request.headers.get("Authorization")
        auth_validated, auth_token = check_api_authorization(auth_header)
        if not auth_validated:
            return (
                jsonify(dict(status=False, message="Invalid Auth")),
                HTTPStatus.BAD_REQUEST,
            )

        req = request.get_json()
        try:
            emission_param = req["emission_param"]
            emission_desc = req["emission_desc"]
            emission_max = req["emission_max"]
        except KeyError as e:
            return (
                jsonify(
                    dict(
                        status=False,
                        message="Invalid Payload. Pass emission_param and emission_max and emission_desc",
                    )
                ),
                HTTPStatus.BAD_REQUEST,
            )

        reg_addr = get_address_from_decoded_token(auth_token)
        reg_data = get_regulator_data_from_storage(reg_addr)
        is_new_emission = True

        print("========== reg data is: ", reg_data)

        if reg_data is not None:
            for d in reg_data:
                if d["data"]["emission_param"] == emission_param:
                    app_id = d.get("app_id")
                    comp_client = ComplianceClient(app_id)
                    is_new_emission = False
                    break

        if is_new_emission:
            comp_client = ComplianceClient()
            reg_data = {
                "app_id": comp_client.get_app_id(),
                "app_address": comp_client.get_app_address(),
                "data": req,
            }
            update_regulator_data_in_storage(reg_addr, reg_data)
            
        final_app_id = comp_client.get_app_id()
        final_app_addr = comp_client.get_app_address()
        return (
            jsonify(
                dict(
                    status=True,
                    message="Created the Emission Control",
                    app_id=final_app_id,
                    app_address=final_app_addr,
                )
            ),
            HTTPStatus.OK,
        )
    except Exception as e:
        return (
            jsonify(
                jsonify(dict(status=False, message=str(e))),
            ),
            HTTPStatus.BAD_GATEWAY,
        )