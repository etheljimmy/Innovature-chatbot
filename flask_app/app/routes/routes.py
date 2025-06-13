from flask import Blueprint, request, jsonify, render_template
from app.services.user_service import process_chat

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('base.html')

@bp.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or not data.get("message") or not data.get("message").strip():
        return jsonify({"response": "Please provide a valid message."}), 400

    user_message = data.get("message", "").strip()
    session_id = data.get("session_id", "default")

    return process_chat(user_message, session_id)
