from http import HTTPStatus
from flask import jsonify, request

from utils.utils import (
    check_api_authorization,
    get_all_regulator_data,
    get_address_from_decoded_token,
)
from compliance_client import ComplianceClient


def mint_compliance_nft():
    """
    Mints the compliance NFT for the given business address.
    Should be called with the business Authorization header
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
        except KeyError as e:
            return (
                jsonify(
                    dict(
                        status=False,
                        message="Invalid Payload. Pass emission_param and emission_value",
                    )
                ),
                HTTPStatus.BAD_REQUEST,
            )

        # get appId for which we need to check the compliance
        app_id = None
        all_data = get_all_regulator_data()
        for k, v in all_data.items():
            for val in v:
                if val["data"]["emission_param"] == emission_param:
                    app_id = val["app_id"]

        if not app_id:
            return (
                jsonify(
                    dict(
                        status=False, message="Could not find emission control"
                    )
                ),
                HTTPStatus.BAD_REQUEST,
            )

        comp_client = ComplianceClient(app_id)
        biz_address = get_address_from_decoded_token(auth_token)
        compliance_nft_res = comp_client.create_compliance_token(biz_address)
        asset_id = compliance_nft_res.return_value

        return (
            jsonify(
                dict(
                    status=True,
                    message="All Good!",
                    nft_id=asset_id,
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
