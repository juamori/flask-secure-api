import datetime
import os
import jwt
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app import models

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    existing = models.User.query.filter_by(username=username).first()
    if existing:
        return jsonify({"error": "user already exists"}), 409

    hashed = generate_password_hash(password)
    user = models.User(username=username, password=hashed)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "user created"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    user = models.User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "invalid credentials"}), 401

    exp = datetime.datetime.utcnow() + datetime.timedelta(seconds=int(os.getenv("JWT_EXP_SECONDS", "3600")))
    payload = {"sub": user.username, "exp": exp}
    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm=current_app.config["JWT_ALGORITHM"])

    return jsonify({"access_token": token}), 200


@auth_bp.route("/protected", methods=["GET"])
def protected():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "missing token"}), 401

    parts = auth_header.split(" ")
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return jsonify({"error": "invalid token"}), 401

    token = parts[1]
    try:
        payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=[current_app.config["JWT_ALGORITHM"]])
        return jsonify({"message": f"Welcome {payload['sub']}!"}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "invalid token"}), 401
