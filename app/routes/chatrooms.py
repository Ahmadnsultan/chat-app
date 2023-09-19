from flask import Blueprint, jsonify
from database import SessionLocal
from models import user_room_relation
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import joinedload
from sqlalchemy import insert
import models


chat_bp = Blueprint('chat_bp', __name__)


@chat_bp.route('/api/chat/rooms/', methods=['GET'])
@jwt_required()
def geta_all_chat_rooms():
    # Retrieve a list of all available chat rooms from database
    session = SessionLocal()
    rooms = session.query(models.ChatRoom).all()
    chat_rooms_data = [{"id": room.id, "name": room.name} for room in rooms]

    return jsonify(chat_rooms_data), 200


@chat_bp.route('/api/chat/rooms/<int:id>/', methods=['GET'])
@jwt_required()
def get_chat_room(id):
    # Retrieve the chat room by its ID from  database
    session = SessionLocal()
    room = session.query(models.ChatRoom).filter_by(id=id).options(joinedload(models.ChatRoom.users)).first()
    if not room:
        return jsonify({"error": "Chat room not found"}), 404

    chat_room_data = {
        "id": room.id,
        "name": room.name,
        "users": [{"id": user.id, "username": user.username} for user in room.users]
    }

    return jsonify(chat_room_data)


@chat_bp.route('/api/chat/rooms/<int:id>/join/', methods=["POST"])
@jwt_required()
def join_chat_room(id):
    session = SessionLocal()

    # Check if the chat room exists
    room = session.query(models.ChatRoom).filter_by(id=id).first()
    if not room:
        session.close()
        return jsonify({"error": "Chat room not found"}), 404

    # Get the current user's information
    user_id = get_jwt_identity()

    user_exist = session.query(user_room_relation).filter_by(room_id=id, user_id=user_id).first()
    # Check if the user is already a member of the chat room
    if user_exist:
        session.close()
        return jsonify({"error": "User is already a member of this chat room"}), 400

    # Add the user to the chat room
    chat_room_user = insert(user_room_relation).values(user_id=user_id, room_id=id)
    session.execute(chat_room_user)
    session.commit()

    session.close()

    return jsonify({"message": "User has joined the chat room successfully"}), 200

