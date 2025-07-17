from functools import wraps
from flask import jsonify, request

from app.models import Note

def self_access_required(f):
    @wraps(f)
    def decorated_function(user, user_id, *args, **kwargs):
        if user.id != user_id:
            return {"message": "You can only access your own account."}, 403
        return f(user, user_id, *args, **kwargs)
    return decorated_function

def owner_required(f):
    @wraps(f)
    def decorated_function(user, note_id, *args, **kwargs):
        note = Note.query.get(note_id)

        if not note:
            return jsonify({"message": "Note not found."}), 404

        if note.user_id != user.id:
            return jsonify({"message": "Note does not belong to you."}), 403

        request.note = note
        return f(user, note_id, *args, **kwargs)
    return decorated_function