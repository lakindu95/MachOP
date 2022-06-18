from datetime import datetime, timedelta
from typing import Union
import logging

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from decouple import config

from app.server.models.authentication import (
    TokenData
)

from app.server.models.machine import (
    MachineModel,
    MachineInDB
)

from app.server.database import (
    retrieve_machine_user
)

# openssl rand -hex 32
SECRET_KEY = config("SECRET_KEY") 
ALGORITHM = config("ALGORITHM")  
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logger = logging.getLogger("uvicorn.error")


# verify the user given password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# get the hash password
def get_password_hash(password):
    return pwd_context.hash(password)


# get machine user from database
def get_user(db, username: str):
    if username in db['username']:
        user_dict = db
        return MachineInDB(**user_dict)


# authenticate machine user
def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# create jwt token
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
   

# get current user from database
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    db_user = await retrieve_machine_user(token_data.username)
    user = get_user(db_user, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


# get active machine user
async def get_current_active_user(current_user: MachineModel = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

