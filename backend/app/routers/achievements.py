from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.app.database import get_db
from backend.app.schemas import AchievementCreate, AchievementOut
import backend.app.crud as crud

router = APIRouter()

# @router.get("/", response_model=List[AchievementOut])
# def read_achievements(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     achievements = crud.get_achievements(db=db, skip=skip, limit=limit)
#     return achievements

# @router.post("/", status_code=status.HTTP_201_CREATED)
# def create_achievement_endpoint(achievement: AchievementCreate, db: Session = Depends(get_db)):
#     new_achievement = crud.create_achievement(db=db, achievement=achievement)
#     return {"status": "success", "achievement": new_achievement}

# @router.get("/{achievement_id}", response_model=AchievementOut)
# def read_achievement(achievement_id: int, db: Session = Depends(get_db)):
#     db_achievement = crud.get_achievement(db, achievement_id)
#     if db_achievement is None:
#         raise HTTPException(status_code=404, detail="Achievement not found")
#     return db_achievement

# @router.put("/{achievement_id}", response_model=AchievementOut)
# def update_achievement_endpoint(achievement_id: int, achievement: AchievementCreate, db: Session = Depends(get_db)):
#     updated_achievement = crud.update_achievement(db, achievement_id, achievement)
#     if updated_achievement is None:
#         raise HTTPException(status_code=404, detail="Achievement not found")
#     return updated_achievement

# @router.delete("/{achievement_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_achievement_endpoint(achievement_id: int, db: Session = Depends(get_db)):
#     deleted = crud.delete_achievement(db, achievement_id)
#     if not deleted:
#         raise HTTPException(status_code=404, detail="Achievement not found")
#     return {"message": "Achievement deleted successfully"}

@router.get("/")
def read_achievements(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    achievements = crud.get_achievements(db=db, skip=skip, limit=limit)
    return {"status": "success", "achievements": achievements}

@router.post("/", status_code=201)
def create_achievement_endpoint(achievement: AchievementCreate, db: Session = Depends(get_db)):
    new_achievement = crud.create_achievement(db=db, achievement=achievement)
    return {"status": "success", "achievement": new_achievement}

@router.get("/{achievement_id}")
def read_achievement(achievement_id: int, db: Session = Depends(get_db)):
    db_achievement = crud.get_achievement(db, achievement_id)
    if db_achievement is None:
        raise HTTPException(status_code=404, detail="Achievement not found")
    return {"status": "success", "achievement": db_achievement}

@router.put("/{achievement_id}")
def update_achievement_endpoint(achievement_id: int, achievement: AchievementCreate, db: Session = Depends(get_db)):
    db_achievement = crud.update_achievement(db, achievement_id, achievement)
    if db_achievement is None:
        raise HTTPException(status_code=404, detail="Achievement not found")
    return {"status": "success", "achievement": db_achievement}

@router.delete("/{achievement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_achievement_endpoint(achievement_id: int, db: Session = Depends(get_db)):
    db_achievement = crud.delete_achievement(db, achievement_id)
    if db_achievement is None:
        raise HTTPException(status_code=404, detail="Achievement not found")
    return {"status": "success", "message": "Achievement deleted successfully"}