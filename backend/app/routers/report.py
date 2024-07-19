from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.app.database import get_db
from backend.app.schemas import ReportCreate, ReportBase, Report
import backend.app.crud as crud

router = APIRouter()

@router.post("/", response_model=Report, status_code=201)
def create_report(report: ReportBase, db: Session = Depends(get_db)):
    created_report = crud.create_report(db=db, report=report)
    if not created_report:
        raise HTTPException(status_code=400, detail="Failed to create report")
    return created_report

@router.get("/", response_model=List[Report])
def read_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_reports(db, skip=skip, limit=limit)

@router.get("/{report_id}", response_model=Report)
def read_report(report_id: int, db: Session = Depends(get_db)):
    db_report = crud.get_report(db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return db_report

@router.put("/{report_id}", response_model=Report)
def update_report(report_id: int, report: ReportBase, db: Session = Depends(get_db)):
    db_report = crud.get_report(db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return crud.update_report(db=db, report_id=report_id, report=report)

@router.delete("/{report_id}", response_model=Report)
def delete_report(report_id: int, db: Session = Depends(get_db)):
    db_report = crud.get_report(db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return crud.delete_report(db=db, report_id=report_id)
