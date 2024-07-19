from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import EmissionFactor, EmissionFactorCreate
import app.crud as crud

router = APIRouter()

@router.post("/", response_model=EmissionFactor, status_code=201)
def create_emission_factor(emission_factor: EmissionFactorCreate, db: Session = Depends(get_db)):
    return crud.create_emission_factor(db=db, emission_factor=emission_factor)

@router.get("/{factor_id}", response_model=EmissionFactor)
def read_emission_factor(factor_id: int, db: Session = Depends(get_db)):
    db_emission_factor = crud.get_emission_factor(db, factor_id)
    if db_emission_factor is None:
        raise HTTPException(status_code=404, detail="Emission Factor not found")
    return db_emission_factor

@router.get("/", response_model=List[EmissionFactor])
def read_emission_factors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_emission_factors(db=db, skip=skip, limit=limit)

@router.delete("/{factor_id}", response_model=EmissionFactor)
def delete_emission_factor(factor_id: int, db: Session = Depends(get_db)):
    db_emission_factor = crud.delete_emission_factor(db=db, factor_id=factor_id)
    if db_emission_factor is None:
        raise HTTPException(status_code=404, detail="Emission Factor not found")
    return db_emission_factor
