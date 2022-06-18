from datetime import timedelta
import logging

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.server.models.authentication import (
    TokenModel
)

from app.server.auth.auth import (
    create_access_token,
    authenticate_user,
)

from app.server.database import (
    retrieve_machine_user
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30
logger = logging.getLogger("uvicorn.error")

router = APIRouter()

# generate token
@router.post("/token", response_model=TokenModel)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):

    db_user = await retrieve_machine_user(form_data.username)
    logger.error(db_user)
    logger.error(form_data.password)

    user = authenticate_user(db_user, form_data.username, form_data.password)
    if not user:
        logger.error("Incorrect username or password")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}