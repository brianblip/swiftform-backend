from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    current_user,
    get_jwt,
    set_access_cookies,
)
from swiftform.database import db
from swiftform.models import TokenBlocklist, User
from datetime import datetime, timezone, timedelta

jwt = JWTManager()


def refresh_expiring_token(response):
    """
    Reset JWT token validity with each request and refresh
    token expiration within 30 minutes of consecutive requests.
    """
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=current_user)
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Return original response even when JWT is invalid
        return response


@jwt.token_in_blocklist_loader
def is_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    """
    Check if JWT exists in database
    """
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None


@jwt.user_lookup_loader
def user_lookup(_jwt_header, jwt_data):
    """
    Attaches a user object when accessing a protected route.

    The user object may be None when is not found in database.
    """
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


@jwt.user_identity_loader
def get_user_id(user):
    return user.id
