import os
import json
from datetime import datetime
from flask import Blueprint, request, jsonify

consent_bp = Blueprint('consent', __name__)

def get_consent_log_path():
    """Lê o caminho do log dinamicamente (respeita variável de ambiente)."""
    env_path = os.getenv("CONSENT_LOG_PATH")
    if env_path:
        return env_path
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base_path, "consent.log")


def log_consent(user_id, policy_version, ip=None):
    """Grava consentimento do usuário em arquivo de log."""
    log_path = get_consent_log_path()
    entry = {
        "user_id": user_id,
        "policy_version": policy_version,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "ip": ip,
    }

    log_dir = os.path.dirname(log_path)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


@consent_bp.route("/consent", methods=["POST"])
def record_consent():
    """Endpoint que grava o consentimento do usuário."""
    data = request.get_json() or {}

    user_id = data.get("user_id")
    version = data.get("version")

    if not user_id or not version:
        return jsonify({"error": "user_id and version required"}), 400

    ip = request.remote_addr
    log_consent(user_id, version, ip)
    return jsonify({"status": "ok"}), 201
