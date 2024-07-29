from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.app.database import get_db
from backend.app.schemas import UserCreate, UserOut,Report, Tip, Goal
import backend.app.crud as crud

router = APIRouter()

@router.get("/", response_model=List[UserOut])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users

# @router.post("/", status_code=status.HTTP_201_CREATED)
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     result = crud.create_user(db=db, user=user)
#     if isinstance(result, dict) and result.get('status') == 'error':
#         raise HTTPException(status_code=400, detail=result['message'])
#     return result
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = crud.create_user(db=db, user=user)
        return new_user
    except ValueError as e:  # Replace with the actual exception type used in crud.create_user
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=UserOut)
def update_user_endpoint(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

# Endpoints for additional functions 
# New Endpoints for Additional Functions
@router.get("/{user_id}/emissions", response_model=float)
def read_user_emissions(user_id: int, db: Session = Depends(get_db)):
    total_emissions = crud.get_user_emissions(db, user_id)
    return total_emissions

@router.post("/{user_id}/emission_report", response_model=Report)
def create_emission_report(user_id: int, db: Session = Depends(get_db)):
    report = crud.generate_emission_report(db, user_id)
    return report

@router.get("/{user_id}/tips", response_model=List[Tip])
def read_tips(user_id: int, db: Session = Depends(get_db)):
    tips = crud.provide_tips_to_user(db, user_id)
    return tips

@router.get("/{user_id}/goal_achievement", response_model=List[Goal])
def read_goal_achievement(user_id: int, db: Session = Depends(get_db)):
    achieved_goals = crud.check_goal_achievement(db, user_id)
    return achieved_goals

