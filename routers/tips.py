from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import TipCreate, Tip, TipBase
import app.crud as crud

router = APIRouter()

@router.get("/", response_model=List[Tip])
def read_tips(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tips = crud.get_tips(db=db, skip=skip, limit=limit)
    return tips

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_tip_endpoint(tip: TipCreate, db: Session = Depends(get_db)):
    new_tip = crud.create_tip(db=db, tip=tip)
    return {"status": "success", "tip": new_tip}

@router.get("/{tip_id}", response_model=Tip)
def read_tip(tip_id: int, db: Session = Depends(get_db)):
    db_tip = crud.get_tip(db, tip_id)
    if db_tip is None:
        raise HTTPException(status_code=404, detail="Tip not found")
    return db_tip

@router.put("/{tip_id}", response_model=Tip)
def update_tip_endpoint(tip_id: int, tip: TipCreate, db: Session = Depends(get_db)):
    updated_tip = crud.update_tip(db, tip_id, tip)
    if updated_tip is None:
        raise HTTPException(status_code=404, detail="Tip not found")
    return updated_tip

@router.delete("/{tip_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tip_endpoint(tip_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_tip(db, tip_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tip not found")
    return {"message": "Tip deleted successfully"}
