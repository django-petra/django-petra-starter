from datetime import datetime, timedelta, UTC
from jose import jwt

# You should store these in environment variables
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 22
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    """
    Decode and verify a JWT token
    Returns the decoded payload if valid, raises JWTError if invalid
    """
    if not token:
        raise jwt.JWTError("Token is missing")
        
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    except jwt.JWTError as e:
        raise jwt.JWTError(f"Invalid token: {str(e)}")