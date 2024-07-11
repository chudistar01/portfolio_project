import functools

from flask import (
    Blueprint, jsonify, g, redirect, render_template, request, session, url_for
    )
from werkzeug.security import check_password_hash, generate_password_hash

from flight_application.db import get_db

user_bp = Blueprint('users', __name__, url_prefix='/users')


@user_bp.route('/login', methods=['POST'])
def register_user():
    data = request.get_json()

    username = data['username']
    password = data['password']
    db = get_db()

    user = db.execute('SELECT * FROM Users WHERE username = ?', (username,)).fetchone()
    db.close()

    if user is None:
        return jsonify({"error": "Invalid username"}), 401

    if not checked_password_hash(user['password'], password):
        return jsonify({"error": "Invalid password"}), 401


