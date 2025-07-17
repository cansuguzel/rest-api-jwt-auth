import datetime
from flask import Blueprint, jsonify, request
from app.utils.tokens import generate_access_token
from config import Config
from app.models import User
from app import db
from app.auth import token_required
from app.decorators import self_access_required

users_bp = Blueprint('users', __name__)

# POST /api/v1/users – Register a new user
@users_bp.route('/', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return {"message": "Username and password required."}, 400

    if User.query.filter_by(username=data['username']).first():
        return {"message": "Username already taken."}, 409

    new_user = User(username=data['username'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()

    return {"message": "User created successfully."}, 201

# POST /api/v1/users/login – User login and create token
@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
       return {"message": "Username and password required."}, 400

    user = User.query.filter_by(username=data.get('username')).first()
    if not user or not user.check_password(data.get('password')):
        return {"message": "Invalid credentials."}, 401

    token = generate_access_token(user.id)
    return jsonify({"token": token}), 200

# GET /api/v1/users – List all users
@users_bp.route('/', methods=['GET'])
@token_required
def get_all_users(user):
    users = User.query.all()
    return jsonify([{"id": u.id, "username": u.username} for u in users])

# GET /api/v1/users/me – Get current user info
@users_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(user):
    return {
        "id": user.id,
        "username": user.username
    }, 200

# PUT /api/v1/users/<user_id> – Update user info
@users_bp.route('/<int:user_id>', methods=['PUT'])
@token_required
@self_access_required
def update_user(user, user_id):
    data = request.get_json()
    if not data:
        return {"message": "No data provided."}, 400
    
    if not data.get("username") and not data.get("password"):
        return {"message": "No fields to update."}, 400
    if data.get("username"):
        existing = User.query.filter_by(username=data["username"]).first()
        if existing and existing.id != user.id:
            return {"message": "Username already taken."}, 409
        user.username = data["username"]


    if data.get("username"):
        user.username = data["username"]
    if data.get("password"):
        user.set_password(data["password"])

    db.session.commit()
    return {
        "message": "User updated.",
        "user": {
            "id": user.id,
            "username": user.username
        }
    }, 200

# DELETE /api/v1/users/<user_id> – Delete user
@users_bp.route('/<int:user_id>', methods=['DELETE'])
@token_required
@self_access_required
def delete_user(user, user_id):
    db.session.delete(user)
    db.session.commit()
    return '', 204