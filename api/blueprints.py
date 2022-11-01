import typing
from flask import Blueprint

from .health import get_health_status
from .user import new_user_registration
from .regulator import create_emission_control, get_all_emission_controls
from .business import check_business_compliance
from .compliance import mint_compliance_nft


"""
BLUEPRINTS FOR REGULATOR API ENDPOINTS
"""


def get_regulator_blueprint():
    """
    Returns the blueprints for all regulator related endpoints
    """
    regulator_blueprint = Blueprint("regulator", __name__)

    @regulator_blueprint.route("/register", methods=["POST"])
    def _register_user():
        return new_user_registration()

    @regulator_blueprint.route("/control", methods=["POST"])
    def _create_emission_control():
        return create_emission_control()

    @regulator_blueprint.route("/controls", methods=["GET"])
    def _get_all_controls():
        return get_all_emission_controls()

    return regulator_blueprint


"""
BLUEPRINTS FOR BUSINESS API ENDPOINTS
"""


def get_business_blueprint():
    """
    Returns the blueprints for all business related endpoints
    """
    biz_blueprint = Blueprint("business", __name__)

    @biz_blueprint.route("/register", methods=["POST"])
    def _register_user():
        return new_user_registration()

    @biz_blueprint.route("/compliant", methods=["POST"])
    def _biz_comliant_check():
        return check_business_compliance()

    return biz_blueprint


"""
BLUEPRINTS FOR COMPLIANCE API ENDPOINTS
"""


def get_compliance_blueprint():
    """
    Returns the blueprints for all compliance related endpoints
    """
    com_blueprint = Blueprint("compliance", __name__)

    @com_blueprint.route("/mint", methods=["POST"])
    def _mint_compliance():
        return mint_compliance_nft()

    return com_blueprint


"""
BLUEPRINTS FOR HEALTH API ENDPOINTS
"""


def get_health_blueprint():
    """
    Returns the blueprints for all server health related endpoints
    """
    health_blueprint = Blueprint("health", __name__)

    @health_blueprint.route("/health", methods=["GET"])
    def _get_health_wrapper():
        return get_health_status()

    return health_blueprint


def get_all_blueprints() -> typing.List[typing.Tuple[Blueprint, str]]:
    """
    Returns a list of all constructed blueprints to the Flask server app
    """
    ret = []
    ret.append((get_health_blueprint(), "/server"))
    ret.append((get_regulator_blueprint(), "/regulator"))
    ret.append((get_business_blueprint(), "/business"))
    ret.append((get_compliance_blueprint(), "/compliance"))
    return ret
