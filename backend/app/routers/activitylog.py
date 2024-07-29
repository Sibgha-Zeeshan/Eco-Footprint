from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.app.database import get_db
from backend.app.schemas import ActivityLogCreate, ActivityLogUpdate, ActivityLog
import backend.app.crud as crud

router = APIRouter()

@router.post("/", response_model=ActivityLog, status_code=201)
def create_activity_log(activity_log: ActivityLogCreate, db: Session = Depends(get_db)):
    created_activity_log = crud.create_activity_log(db=db, activity_log=activity_log)
    if not created_activity_log:
        raise HTTPException(status_code=400, detail="Failed to create activity log")
    return created_activity_log

@router.get("/", response_model=list[ActivityLog])
def read_activity_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_activity_logs(db, skip=skip, limit=limit)

@router.get("/{log_id}", response_model=ActivityLog)
def read_activity_log(log_id: int, db: Session = Depends(get_db)):
    db_activity_log = crud.get_activity_log(db, log_id=log_id)
    if db_activity_log is None:
        raise HTTPException(status_code=404, detail="Activity log not found")
    return db_activity_log

@router.put("/{log_id}", response_model=ActivityLog)
def update_activity_log(log_id: int, activity_log: ActivityLogUpdate, db: Session = Depends(get_db)):
    db_activity_log = crud.get_activity_log(db, log_id=log_id)
    if db_activity_log is None:
        raise HTTPException(status_code=404, detail="Activity log not found")
    return crud.update_activity_log(db=db, log_id=log_id, activity_log=activity_log)

@router.delete("/{log_id}", response_model=ActivityLog)
def delete_activity_log(log_id: int, db: Session = Depends(get_db)):
    db_activity_log = crud.get_activity_log(db, log_id=log_id)
    if db_activity_log is None:
        raise HTTPException(status_code=404, detail="Activity log not found")
    return crud.delete_activity_log(db=db, log_id=log_id)


