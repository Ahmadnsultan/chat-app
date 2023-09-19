from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from database import SessionLocal
import utils, models
from datetime import timedelta, timezone
from datetime import datetime


login_bp = Blueprint('login', __name__)
logout_bp = Blueprint('logout', __name__)


@login_bp.route('/api/login/', methods=['POST'])
def login():
    user_credentials = request.form
    session = SessionLocal()
    user = session.query(models.User).filter(
        models.User.username == user_credentials['username']).first()

    if not user:
        session.close()
        return jsonify({"error": "Invalid Credentials"}), 403

    if not utils.verify(user_credentials["password"], user.password):
        session.close()
        return jsonify({"error": "invalid credentials"})

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200


# Endpoint for revoking the current users access token. Saved the unique
# identifier (jti) for the JWT into our database.
@logout_bp.route('/api/logout/', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    session = SessionLocal()
    session.add(models.TokenBlocklist(jti=jti, created_at=now))
    session.commit()
    return jsonify(msg="JWT revoked")
