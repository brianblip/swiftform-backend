import datetime
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    current_user,
    get_jwt,
    set_access_cookies,
)
from swiftform.database import db
from swiftform.models import TokenBlocklist, User

jwt = JWTManager()


def refresh_expiring_token(response):
    """
    Reset JWT token validity with each request and refresh
    token expiration within 30 minutes of consecutive requests.
    """
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(datetime.timezone.utc)
        target_timestamp = datetime.timestamp(
            now + datetime.timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=current_user)
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Return original response even when JWT is invalid
        return response
