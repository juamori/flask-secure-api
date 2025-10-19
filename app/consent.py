import os
import json
from datetime import datetime
from flask import Blueprint, request, jsonify

consent_bp = Blueprint('consent_bp', __name__)

@consent_bp.route('/consent', methods=['POST'])
def record_consent():
    """
    Endpoint para registrar o consentimento do usuário.
    Grava um log em um arquivo especificado pela variável de ambiente CONSENT_LOG_PATH.
    """
    data = request.get_json()
    if not data or 'user_id' not in data or 'version' not in data:
        return jsonify({"error": "user_id and version are required"}), 400

    log_path = os.environ.get('CONSENT_LOG_PATH', 'consent.log')

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": data.get('user_id'),
        "version": data.get('version'),
        "event": "consent_given"
    }

    try:
        log_dir = os.path.dirname(log_path)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        
        with open(log_path, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
            
    except Exception as e:
        print(f"ERRO: Não foi possível escrever no arquivo de log: {e}")
        return jsonify({"error": "Internal server error writing log"}), 500

    return jsonify({"status": "ok"}), 201