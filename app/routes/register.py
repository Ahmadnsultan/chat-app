from flask import request, jsonify
from database import SessionLocal
from models import User
from flask import Blueprint
from utils import hash


register_bp = Blueprint('register', __name__)


@register_bp.route('/api/register/', methods=['POST'])
def create_user():
    data = request.json

    if 'username' not in data or 'password' not in data:
        return jsonify({"error": "Username and password are required"}), 400

    username = data['username']
    password = data['password']

    session = SessionLocal()

    # Check if the username is already taken
    existing_user = session.query(User).filter_by(username=username).first()
    if existing_user:
        session.close()
        return jsonify({"error": "Username already exists"}), 400

    password_hash = hash(password)

    # Create a new user and add it to the database
    new_user = User(username=username, password=password_hash)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    user_dict = {
        "id": new_user.id,
        "username": new_user.username,
    }

    return jsonify(user_dict), 201
