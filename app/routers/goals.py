from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import Goal, GoalCreate, GoalUpdate
import app.crud as crud

router = APIRouter()

@router.post("/", response_model=Goal, status_code=201)
def create_goal(goal: GoalCreate, db: Session = Depends(get_db)):
    created_goal = crud.create_goal(db=db, goal=goal)
    return created_goal

@router.get("/", response_model=List[Goal])
def read_goals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_goals(db, skip=skip, limit=limit)

@router.get("/{goal_id}", response_model=Goal)
def read_goal(goal_id: int, db: Session = Depends(get_db)):
    db_goal = crud.get_goal(db, goal_id=goal_id)
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    return db_goal

@router.put("/{goal_id}", response_model=Goal)
def update_goal(goal_id: int, goal: GoalUpdate, db: Session = Depends(get_db)):
    db_goal = crud.get_goal(db, goal_id=goal_id)
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    return crud.update_goal(db=db, goal_id=goal_id, goal=goal)

@router.delete("/{goal_id}", response_model=Goal)
def delete_goal(goal_id: int, db: Session = Depends(get_db)):
    db_goal = crud.get_goal(db, goal_id=goal_id)
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    return crud.delete_goal(db=db, goal_id=goal_id)
