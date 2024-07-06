from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal, engine, Base, get_db
from app.models import User
from app.schemas import UserCreate, UserOut
import app.crud as crud

app = FastAPI()


# Root Endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Environment Impact Tracker API"}

# Users Endpoints----------------------------------------------
@app.get("/users/", response_model=List[UserOut])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users

@app.post("/users/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    result = crud.create_user(db=db, user=user)
    if isinstance(result, dict) and result.get('status') == 'error':
        raise HTTPException(status_code=400, detail=result['message'])
    return result


@app.get("/users/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=UserOut)
def update_user_endpoint(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}





