import json

from http import HTTPStatus
from flask import jsonify, request

from utils.utils import (
    check_api_authorization,
    get_address_from_decoded_token,
    get_regulator_data_from_storage,
    update_regulator_data_in_storage,
)

from compliance_client import ComplianceClient


def _create_get_emission_control(app_id: int = 0):
    if app_id == 0:
        return ComplianceClient()
    return ComplianceClient(app_id)


def get_all_emission_controls():
    """
    Get all Emission Controls for the regulator given
    """
    try:
        auth_header = request.headers.get("Authorization")
        auth_validated, auth_token = check_api_authorization(auth_header)
        if not auth_validated:
            return (
                jsonify(dict(status=False, message="Invalid Auth")),
                HTTPStatus.BAD_REQUEST,
            )
        reg_addr = get_address_from_decoded_token(auth_token)
        all_reg_data = get_regulator_data_from_storage(reg_addr)
        all_apps = []
        for d in all_reg_data:
            all_apps.append(
                {
                    "app_id": d["app_id"],
                    "emission_param": d["data"]["emission_param"],
                    "emission_desc": d["data"]["emission_desc"],
                    "emission_max": d["data"]["emission_max"],
                }
            )
        return (
            jsonify(dict(status=True, message="All Good!", controls=all_apps)),
            HTTPStatus.OK,
        )
    except Exception as e:
        return (
            jsonify(
                jsonify(dict(status=False, message=str(e))),
            ),
            HTTPStatus.BAD_GATEWAY,
        )


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
        if reg_data is not None:
            for d in reg_data:
                if d["data"]["emission_param"] == emission_param:
                    app_id = d.get("app_id")
                    comp_client = ComplianceClient(app_id)
                    new_reg_data = {
                        "app_id": comp_client.get_app_id(),
                        "app_address": comp_client.get_app_address(),
                        "data": req,
                    }
                    update_regulator_data_in_storage(reg_addr, new_reg_data)
                    is_new_emission = False
                    break

        if is_new_emission:
            comp_client = ComplianceClient()
            new_reg_data = {
                "app_id": comp_client.get_app_id(),
                "app_address": comp_client.get_app_address(),
                "data": req,
            }
            update_regulator_data_in_storage(
                reg_addr, new_reg_data, new_data=True
            )

        final_app_id = comp_client.get_app_id()
        final_app_addr = comp_client.get_app_address()
        set_txn_res = comp_client.set_emissions_rule(
            f"{emission_param}:{emission_desc}", int(emission_max)
        )
        return (
            jsonify(
                dict(
                    status=True,
                    message="Created the Emission Control",
                    app_id=final_app_id,
                    app_address=final_app_addr,
                    app_set_txn=set_txn_res.tx_id,
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
