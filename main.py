from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import TipBase, Tip,Report, ReportBase,EmissionFactor, EmissionFactorCreate,UserCreate, UserOut, AchievementCreate,  AchievementOut, ActivityLogCreate, ActivityLogUpdate, ActivityLog, Goal, GoalCreate, GoalUpdate
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

# ActivityLog endpoints
@app.post("/activity_logs/", response_model=ActivityLog, status_code=201)
def create_activity_log(activity_log: ActivityLogCreate, db: Session = Depends(get_db)):
    created_activity_log = crud.create_activity_log(db=db, activity_log=activity_log)
    if not created_activity_log:
        raise HTTPException(status_code=400, detail="Failed to create activity log")
    return created_activity_log

@app.get("/activity_logs/", response_model=list[ActivityLog])
def read_activity_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_activity_logs(db, skip=skip, limit=limit)

@app.get("/activity_logs/{log_id}", response_model=ActivityLog)
def read_activity_log(log_id: int, db: Session = Depends(get_db)):
    db_activity_log = crud.get_activity_log(db, log_id=log_id)
    if db_activity_log is None:
        raise HTTPException(status_code=404, detail="Activity log not found")
    return db_activity_log

@app.put("/activity_logs/{log_id}", response_model=ActivityLog)
def update_activity_log(log_id: int, activity_log: ActivityLogUpdate, db: Session = Depends(get_db)):
    db_activity_log = crud.get_activity_log(db, log_id=log_id)
    if db_activity_log is None:
        raise HTTPException(status_code=404, detail="Activity log not found")
    return crud.update_activity_log(db=db, log_id=log_id, activity_log=activity_log)

@app.delete("/activity_logs/{log_id}", response_model=ActivityLog)
def delete_activity_log(log_id: int, db: Session = Depends(get_db)):
    db_activity_log = crud.get_activity_log(db, log_id=log_id)
    if db_activity_log is None:
        raise HTTPException(status_code=404, detail="Activity log not found")
    return crud.delete_activity_log(db=db, log_id=log_id)

#  End points of Emission Factor --------------------------------------------------------------------------------------------
@app.post("/emission_factors/", response_model=EmissionFactor, status_code=201)
def create_emission_factor(emission_factor: EmissionFactorCreate, db: Session = Depends(get_db)):
    return crud.create_emission_factor(db=db, emission_factor=emission_factor)

@app.get("/emission_factors/{factor_id}", response_model=EmissionFactor)
def read_emission_factor(factor_id: int, db: Session = Depends(get_db)):
    db_emission_factor = crud.get_emission_factor(db, factor_id)
    if db_emission_factor is None:
        raise HTTPException(status_code=404, detail="Emission Factor not found")
    return db_emission_factor

@app.get("/emission_factors/", response_model=List[EmissionFactor])
def read_emission_factors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_emission_factors(db=db, skip=skip, limit=limit)

@app.delete("/emission_factors/{factor_id}", response_model=EmissionFactor)
def delete_emission_factor(factor_id: int, db: Session = Depends(get_db)):
    db_emission_factor = crud.delete_emission_factor(db=db, factor_id=factor_id)
    if db_emission_factor is None:
        raise HTTPException(status_code=404, detail="Emission Factor not found")
    return db_emission_factor

# Goal endpoints -------------------------------------------------------------------------------------------------
@app.post("/goals/", response_model=Goal, status_code=201)
def create_goal(goal: GoalCreate, db: Session = Depends(get_db)):
    created_goal = crud.create_goal(db=db, goal=goal)
    return created_goal

@app.get("/goals/", response_model=list[Goal])
def read_goals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_goals(db, skip=skip, limit=limit)

@app.get("/goals/{goal_id}", response_model=Goal)
def read_goal(goal_id: int, db: Session = Depends(get_db)):
    db_goal = crud.get_goal(db, goal_id=goal_id)
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    return db_goal

@app.put("/goals/{goal_id}", response_model=Goal)
def update_goal(goal_id: int, goal: GoalUpdate, db: Session = Depends(get_db)):
    db_goal = crud.get_goal(db, goal_id=goal_id)
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    return crud.update_goal(db=db, goal_id=goal_id, goal=goal)

@app.delete("/goals/{goal_id}", response_model=Goal)
def delete_goal(goal_id: int, db: Session = Depends(get_db)):
    db_goal = crud.get_goal(db, goal_id=goal_id)
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    return crud.delete_goal(db=db, goal_id=goal_id)

# Acheivement log Endpoints Endpoints----------------------------------------------
@app.get("/achievements/")
def read_achievements(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    achievements = crud.get_achievements(db=db, skip=skip, limit=limit)
    return {"status": "success", "achievements": achievements}

@app.post("/achievements/", status_code=status.HTTP_201_CREATED)
def create_achievement_endpoint(achievement: AchievementCreate, db: Session = Depends(get_db)):
    new_achievement = crud.create_achievement(db=db, achievement=achievement)
    return {"status": "success", "achievement": new_achievement}

@app.get("/achievements/{achievement_id}")
def read_achievement(achievement_id: int, db: Session = Depends(get_db)):
    db_achievement = crud.get_achievement(db, achievement_id)
    if db_achievement is None:
        raise HTTPException(status_code=404, detail="Achievement not found")
    return {"status": "success", "achievement": db_achievement}

@app.put("/achievements/{achievement_id}")
def update_achievement_endpoint(achievement_id: int, achievement: AchievementCreate, db: Session = Depends(get_db)):
    db_achievement = crud.update_achievement(db, achievement_id, achievement)
    if db_achievement is None:
        raise HTTPException(status_code=404, detail="Achievement not found")
    return {"status": "success", "achievement": db_achievement}

@app.delete("/achievements/{achievement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_achievement_endpoint(achievement_id: int, db: Session = Depends(get_db)):
    db_achievement = crud.delete_achievement(db, achievement_id)
    if db_achievement is None:
        raise HTTPException(status_code=404, detail="Achievement not found")
    return {"status": "success", "message": "Achievement deleted successfully"}

# Report End Points -------------------------------------------------------------------------------------------
@app.post("/reports/", response_model= Report, status_code=201)
def create_report(report: ReportBase, db: Session = Depends(get_db)):
    return crud.create_report(db, report)

@app.get("/reports/", response_model=List[Report])
def read_reports(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_reports(db, skip=skip, limit=limit)

@app.get("/reports/{report_id}", response_model= Report)
def read_report(report_id: int, db: Session = Depends(get_db)):
    db_report = crud.get_report(db, report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return db_report

@app.put("/reports/{report_id}", response_model= Report)
def update_report(report_id: int, report: ReportBase, db: Session = Depends(get_db)):
    db_report = crud.update_report(db, report_id, report)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return db_report

@app.delete("/reports/{report_id}", response_model= Report)
def delete_report(report_id: int, db: Session = Depends(get_db)):
    db_report = crud.delete_report(db, report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return db_report

# Tip End Points -----------------------------------------------------------------------------------------------
@app.post("/tips/", response_model=Tip, status_code=201)
def create_tip(tip: TipBase, db: Session = Depends(get_db)):
    return crud.create_tip(db, tip)

@app.get("/tips/", response_model=List[Tip])
def read_tips(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_tips(db, skip=skip, limit=limit)

@app.get("/tips/{tip_id}", response_model= Tip)
def read_tip(tip_id: int, db: Session = Depends(get_db)):
    db_tip = crud.get_tip(db, tip_id)
    if db_tip is None:
        raise HTTPException(status_code=404, detail="Tip not found")
    return db_tip

@app.put("/tips/{tip_id}", response_model=Tip)
def update_tip(tip_id: int, tip: TipBase, db: Session = Depends(get_db)):
    db_tip = crud.update_tip(db, tip_id, tip)
    if db_tip is None:
        raise HTTPException(status_code=404, detail="Tip not found")
    return db_tip

@app.delete("/tips/{tip_id}", response_model=Tip)
def delete_tip(tip_id: int, db: Session = Depends(get_db)):
    db_tip = crud.delete_tip(db, tip_id)
    if db_tip is None:
        raise HTTPException(status_code=404, detail="Tip not found")
    return db_tip
