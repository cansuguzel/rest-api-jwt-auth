from functools import wraps
from flask import request, jsonify
from app.utils.tokens import decode_token
from app.models import User

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"message": "Authorization header missing or invalid."}), 401

        token = auth_header.split(" ")[1]
        payload, error = decode_token(token)

        if error:
            return jsonify({"message": error}), 401

        user = User.query.get(payload.get("user_id"))
        if not user:
            return jsonify({"message": "User not found."}), 404

        return f(user=user, *args, **kwargs)

    return decorated_function



