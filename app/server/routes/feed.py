from datetime import datetime, timedelta
from typing import Union

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


from app.server.database import (
    add_sensor_feed,
    delete_sensor_feed,
    retrieve_sensor_feed,
    retrieve_sensor_feeds,
    retrieve_sensor_feeds_by_start_date,
    update_sensor_feed,
)
from app.server.models.feed import (
    ErrorResponseModel,
    ResponseModel,
    MachOPSchema,
    UpdateMachOPModel,
    UserModel,
    UserInDB,
    TokenModel,
    TokenData
)

router = APIRouter()

@router.post("/", response_description="Machine data added into the database")
async def add_sensor_feed_data(feed: MachOPSchema = Body(...)):
    feed = jsonable_encoder(feed)
    new_feed = await add_sensor_feed(feed)
    return ResponseModel(new_feed, "Machine feed added successfully.")


@router.get("/", response_description="Machine retrieved")
async def get_feeds(token: str = Depends(oauth2_scheme)):
    feeds = await retrieve_sensor_feeds()
    if feeds:
        return ResponseModel(feeds, "Machine feed retrieved successfully")
    return ResponseModel(feeds, "Empty list returned")

@router.get("/startdate/{start_date}", response_description="Data retrieved from start date")
async def get_feeds_by_start_date(start_date):
    feeds = await retrieve_sensor_feeds_by_start_date(start_date)
    if feeds:
        return ResponseModel(feeds, "Machine feed retrieved successfully")
    return ResponseModel(feeds, "Empty list returned")


@router.get("/{id}", response_description="Machine feed retrieved")
async def get_feed_data(id):
    feed = await retrieve_sensor_feed(id)
    if feed:
        return ResponseModel(feed, "Machine feed retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Machine doesn't exist.")

@router.put("/{id}")
async def update_feed_data(id: str, req: UpdateMachOPModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_feed = await update_sensor_feed(id, req)
    if updated_feed:
        return ResponseModel(
            "Machine with ID: {} name update is successful".format(id),
            "Machine feed updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the machine feed.",
    )

@router.delete("/{id}", response_description="feed data deleted from the database")
async def delete_sensor_feed_data(id: str):
    deleted_feed = await delete_sensor_feed(id)
    if deleted_feed:
        return ResponseModel(
            "feed with ID: {} removed".format(id), "feed deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "feed with id {0} doesn't exist".format(id)
    )


# User APIs 

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
   
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
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: UserModel = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token", response_model=TokenModel)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
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

@router.get("/users/me/", response_model=UserModel)
async def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(current_user: UserModel = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]