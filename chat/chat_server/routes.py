from flask import Blueprint, jsonify, request
from .db import get_db

from .models import User
from .auth import hash_password
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
api_bp = Blueprint("api", __name__, url_prefix="/api/v1")


@api_bp.route("/auth/register", methods=["POST"])
def register():
    logger.info("[Distributed Chat] Inside user registration")
    data = request.get_json()
    if not data:
        return jsonify({"error": "username and password is required"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not isinstance(username, str):
        logger.info(f"[Distributed Chat] username is empty {username}")
        return jsonify({"error": "username is required"}), 400

    if not password or not isinstance(password, str):
        logger.info("[Distributed Chat] password is empty")
        return jsonify({"error": "password is required"}), 400

    username = username.strip()
    if len(username) < 3 or len(username) > 50:
        logger.info("[Distributed Chat] username {username} fails length validation")
        return jsonify({"error": "username must be between 3 and 50 characters"}), 400

    password = password.strip()
    if len(password) < 6:
        logger.info("[Distributed Chat] password fails length validation")
        return jsonify({"error": "password must be atleast 6 characters"}), 400

    session = get_db()
    try:
        existing_user = session.query(User).filter(User.username == username).first()
        if existing_user:
            logger.info("[Distributed Chat] username {username} exists")
            return jsonify({"error": "username is already taken"}), 409
        user = User(
            username=username,
            password_hash=hash_password(password),
        )
        session.add(user)
        session.commit()
        logger.info("[Distributed Chat] username {username} created")
        session.refresh(user)

        return jsonify(
            {
                "user_id": user.id,
                "username": user.username,
                "created_at": user.created_at.isoformat(),
            }
        ), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": {e}}), 500
        logger.info("[Distributed Chat] username {username} creation failed")

    finally:
        session.close()
