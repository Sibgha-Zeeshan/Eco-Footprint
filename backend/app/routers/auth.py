from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from backend.app.schemas import UserCreate, UserOut
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from typing import List
from backend.app.database import get_db
from backend.app.schemas import UserCreate, UserOut
import backend.app.crud as crud
from fastapi.security import OAuth2PasswordRequestForm
import logging

# Google Authentication  
# from fastapi.security import OAuth2AuthorizationCodeBearer
# from authlib.integrations.starlette_client import OAuth, OAuthError
# from starlette.requests import Request
# from starlette.responses import RedirectResponse
# from dotenv import load_dotenv


router = APIRouter()


# Define JWT secret key and algorithm
SECRET_KEY = "simpletestkey12345"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Use argon2 for password hashing
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(datetime.UTC) + expires_delta
    else:
        expire = datetime.now(datetime.UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = crud.get_user_by_email(db, user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = get_password_hash(user.password)
        user.password = hashed_password

        new_user = crud.create_user(db=db, user=user)
        return UserOut.model_validate(new_user)  # Using Pydantic model for serialization

    except HTTPException as http_exc:
        logging.error(f"HTTP error during user registration: {http_exc.detail}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error during user registration: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    
@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, form_data.username)
    if not db_user or not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": db_user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}





# Logging the errors here 
logging.basicConfig(level=logging.DEBUG)