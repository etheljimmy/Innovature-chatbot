from flask import Blueprint, request, jsonify, render_template, send_from_directory, current_app
from app.services.user_service import process_chat
import os
bp = Blueprint('main', __name__)
@bp.route('/chat', methods=['POST'])
def chat():
    return process_chat()

