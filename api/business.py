from http import HTTPStatus
from flask import jsonify, request

from utils.utils import check_api_authorization, get_all_regulator_data
from utils.constants import REGULATOR_FILE
from compliance_client import ComplianceClient

def check_business_compliance():
    """
    Checks whether the business is compliant to an emission control or not
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
            emission_value = req["emission_value"]
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
        param = ""
        all_data = get_all_regulator_data()
        for k, v in all_data.items():
            for val in v:
                if val["data"]["emission_param"] == emission_param:
                    app_id = val["app_id"]
                    param = f"{val['data']['emission_param']}:{val['data']['emission_desc']}"

        if not app_id:
            return (
                jsonify(dict(status=False, message="Could not find emission control")),
                HTTPStatus.BAD_REQUEST,
            )

        print("===== appId being used for compliance: ", app_id, param, emission_value)
        comp_client = ComplianceClient(app_id)
        complient_resp = comp_client.is_business_compliant(param, emission_value)
        return (
            jsonify(dict(status=True, message="All Good!", is_compliant=complient_resp.return_value)),
            HTTPStatus.OK,
        )
    except Exception as e:
        return (
            jsonify(
                jsonify(dict(status=False, message=str(e))),
            ),
            HTTPStatus.BAD_GATEWAY,
        )
