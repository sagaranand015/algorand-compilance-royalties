import flask
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from pathlib import Path

from api.blueprints import get_all_blueprints
from utils.constants import AUTH_FILE, REGULATOR_FILE, BUSINESS_FILE


def create_server():
    """
    Method to create the server instance for serving the REST API Endpoints
    """

    app = Flask(__name__)
    CORS(app)
    for bp, pref in get_all_blueprints():
        app.register_blueprint(bp, url_prefix=pref)

    return app


if __name__ == "__main__":
    server = create_server()

    auth_file = Path(AUTH_FILE)
    if not auth_file.exists():
        with open(AUTH_FILE, "w") as fp:
            fp.write("{}")

    regulator_file = Path(REGULATOR_FILE)
    if not regulator_file.exists():
        with open(REGULATOR_FILE, "w") as fp1:
            fp1.write("{}")

    biz_file = Path(BUSINESS_FILE)
    if not biz_file:
        with open(BUSINESS_FILE, "w") as fp2:
            fp2.write("{}")

    server.run(
        host="0.0.0.0",
        port=8080,
        debug=False,
        use_reloader=False,
    )
