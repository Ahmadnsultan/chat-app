from flask import Flask, jsonify
from routes.register import register_bp
from routes.auth import login_bp, logout_bp
from routes.chatrooms import chat_bp
from routes.messages import message_bp
import models
from database import engine, SessionLocal
from flask_jwt_extended import JWTManager
from datetime import timedelta
from config import settings

app = Flask(__name__)


app.config['JWT_SECRET_KEY'] = settings.jwt_secret_key
app.config['JWT_ALGORITHM'] = settings.jwt_algorithm
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=settings.jwt_access_token_expires)

jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    session = SessionLocal()
    token = session.query(models.TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None


models.Base.metadata.create_all(bind=engine)


@app.route("/", methods=["GET"])
def hello():
    return jsonify({"data": "hello world"}), 200


app.register_blueprint(register_bp)
app.register_blueprint(login_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(message_bp)

if __name__ == '__main__':
    app.run(debug=True)