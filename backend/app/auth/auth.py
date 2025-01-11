import secrets
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.db import session
from app.auth import utils
from app.api import crud

SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTE = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        db = session.SessionLocal()
        user = crud.get_user_by_username(db, username)
        if user is  None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

