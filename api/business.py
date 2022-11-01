from http import HTTPStatus
from flask import jsonify


def get_health_status():
    """
    Demo Endpoints for returning the health status of the DApp backend
    """
    try:
        return (
            jsonify(dict(status=True, message="All Good!")),
            HTTPStatus.OK,
        )
    except Exception as e:
        return (
            jsonify(
                jsonify(dict(status=False, message=str(e))),
            ),
            HTTPStatus.BAD_GATEWAY,
        )
