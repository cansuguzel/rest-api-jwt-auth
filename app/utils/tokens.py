from datetime import datetime, timedelta
import jwt
from config import Config 

# Utility function to generate an access token
def generate_access_token(user_id, expires_minutes=20):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=expires_minutes)
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
    
    return token

# Utility function to decode a token
def decode_token(token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return payload, None
    except jwt.ExpiredSignatureError:
        return None, "Your session has expired. Please log in again."
    except jwt.InvalidTokenError:
        return None, "Invalid authentication token. Please log in again."