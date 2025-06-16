from flask import Blueprint, request, jsonify, render_template, send_from_directory, current_app
from app.services.user_service import process_chat
import os

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('base.html')

@bp.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or not data.get("message") or not data.get("message").strip():
            current_app.logger.warning("Invalid message received in /chat endpoint.")
            return jsonify({"response": "Please provide a valid message."}), 400

        user_message = data.get("message", "").strip()
        session_id = data.get("session_id", "default")

        return process_chat(user_message, session_id)
    except Exception as e:
        current_app.logger.error(f"Exception in /chat endpoint: {e}", exc_info=True)
        return jsonify({"response": "Internal server error."}), 500

# Serve React static files in production
@bp.route('/<path:path>', methods=['GET'])
def serve_react(path):
    react_build_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../react/dist'))
    if os.path.exists(os.path.join(react_build_dir, path)):
        return send_from_directory(react_build_dir, path)
    return send_from_directory(react_build_dir, 'index.html')
