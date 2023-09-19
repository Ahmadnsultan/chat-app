from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

# table that create many to many relation between user and chat room
# used to allow use to join a chat room
user_room_relation = Table(
    "user_room_relation",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("room_id", ForeignKey("chat_room.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    chatrooms = relationship("ChatRoom", secondary=user_room_relation, back_populates="users")


# model that stores the revoked token in database during logout
class TokenBlocklist(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True)
    jti = Column(String(36), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False)


class ChatRoom(Base):
    __tablename__ = "chat_room"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    users = relationship("User", secondary=user_room_relation, back_populates="chatrooms")



class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, nullable=False)
    text = Column(String, nullable=False)
    sender_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    room_id = Column(Integer, ForeignKey("chat_room.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


