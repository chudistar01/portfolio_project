import functools

from flask import (
    Blueprint, jsonify, g, redirect, render_template, request, session, url_for
    )
from werkzeug.security import check_password_hash, generate_password_hash

from flight_application.db import get_db

user_bp = Blueprint('users', __name__, url_prefix='/users')


@user_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required'}), 400

    username = data['username']
    password = data['password']
    role = data.get('role', 'user')
    db = get_db()

    hashed_password = generate_password_hash(password)

    try:
        db.execute(
                'INSERT INTO Users (username, password, role) VALUES (?, ?, ?)',
                (username, hashed_password, role)
                )
        db.commit()

        return jsonify({'message': 'User registered successfully'}), 201

    except db.IntegrityError:
        return jsonify({'error': f'User {username} is already registered.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
