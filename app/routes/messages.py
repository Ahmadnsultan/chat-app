from flask import jsonify, request, Blueprint
from database import SessionLocal
from flask_jwt_extended import jwt_required, get_jwt_identity
import models


message_bp = Blueprint("message", __name__)


@message_bp.route('/api/chat/rooms/<int:id>/messages/', methods=['POST'])
@jwt_required()
def send_message(id):
    current_user_id = get_jwt_identity()
    # Retrieve the chat room by its ID from  database
    session = SessionLocal()
    room = session.query(models.ChatRoom).filter_by(id=id).first()

    if room is None:
        return jsonify({"error": "Chat room not found"}), 404

    # check if current user has joined the chat room
    check_user_join = session.query(models.user_room_relation).filter(
        current_user_id == models.user_room_relation.c.user_id, models.user_room_relation.c.room_id == id).first()
    if not check_user_join:
        return jsonify({"warning": "please first join the chat room"})

    # Get the message data from the request JSON
    data = request.json
    message_text = data.get("text")

    if not message_text :
        return jsonify({"error": "Message text and sender ID are required"}), 400
    # Get the user id from jwt header

    # Create a new message and add it to the chat room
    new_message = models.Message(text=message_text, sender_id=current_user_id, room_id=id)
    session = SessionLocal()
    session.add(new_message)
    session.commit()

    return jsonify({"message": "Message sent successfully"}), 201


@message_bp.route('/api/chat/rooms/<int:id>/messages/', methods=['GET'])
@jwt_required()
def get_message(id):
    session = SessionLocal()
    room = session.query(models.ChatRoom).filter_by(id=id).first()

    if room is None:
        session.close()
        return jsonify({"error": "Chat room not found"}), 404

    current_user_id = get_jwt_identity()

    check_user_join = session.query(models.user_room_relation).filter(
        current_user_id == models.user_room_relation.c.user_id, models.user_room_relation.c.room_id == id).first()
    if not check_user_join:
        return jsonify({"warning": "please first join the chat room"}), 403

    messages = session.query(models.Message).filter_by(room_id=id).all()

    if not messages:
        session.close()
        return jsonify({"data": "empty chat"}), 404

    message_details = [{"sender_id": message.sender_id, "room_id": message.room_id, "text": message.text, "created_at": message.created_at} for message in messages]
    return jsonify({"messages": message_details}), 200

