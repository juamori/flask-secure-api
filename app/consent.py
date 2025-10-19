import os
import json
from datetime import datetime
from flask import Blueprint, request, jsonify

consent_bp = Blueprint('consent_bp', __name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONSENT_LOG = os.getenv("CONSENT_LOG_PATH", os.path.join(BASE_DIR, "..", "consent.log"))
CONSENT_LOG = os.path.abspath(CONSENT_LOG)

@consent_bp.route('/consent', methods=['POST'])
def record_consent():
    data = request.get_json()
    if not data or 'user_id' not in data or 'version' not in data:
        return jsonify({"error": "user_id and version are required"}), 400

    user_id = data['user_id']
    version = data['version']
    log_entry = {
        "user_id": user_id,
        "policy_version": version,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    try:
        log_dir = os.path.dirname(CONSENT_LOG)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        with open(CONSENT_LOG, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
    except Exception as e:
        print(f"ERRO: Não foi possível escrever no arquivo de log: {e}")
        return jsonify({"error": "Internal server error writing log"}), 500

    return jsonify({"status": "ok"}), 201
