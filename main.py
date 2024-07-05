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
    if result['status'] == 'error':
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

# Activity log Endpoints Endpoints----------------------------------------------

# # @app.post("/activity_logs/", response_model=ActivityLogOut, status_code=status.HTTP_201_CREATED)
# # def create_activity_log(activity_log: ActivityLogCreate, db: Session = Depends(get_db)):
# #     db_activity_log = ActivityLog(user_id=activity_log.user_id, activity_type=activity_log.activity_type, activity_value=activity_log.activity_value, date=activity_log.date)
# #     db.add(db_activity_log)
# #     db.commit()
# #     db.refresh(db_activity_log)
# #     return db_activity_log

# # @app.get("/activity_logs/{log_id}", response_model=ActivityLogOut)
# # def read_activity_log(log_id: int, db: Session = Depends(get_db)):
# #     db_activity_log = db.query(ActivityLog).filter(ActivityLog.log_id == log_id).first()
# #     if db_activity_log is None:
# #         raise HTTPException(status_code=404, detail="Activity log not found")
# #     return db_activity_log

# # @app.put("/activity_logs/{log_id}", response_model=ActivityLogOut)
# # def update_activity_log(log_id: int, activity_log: ActivityLogCreate, db: Session = Depends(get_db)):
# #     db_activity_log = db.query(ActivityLog).filter(ActivityLog.log_id == log_id).first()
# #     if db_activity_log is None:
# #         raise HTTPException(status_code=404, detail="Activity log not found")
# #     db_activity_log.user_id = activity_log.user_id
# #     db_activity_log.activity_type = activity_log.activity_type
# #     db_activity_log.activity_value = activity_log.activity_value
# #     db_activity_log.date = activity_log.date
# #     db.commit()
# #     db.refresh(db_activity_log)
# #     return db_activity_log

# # @app.delete("/activity_logs/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
# # def delete_activity_log(log_id: int, db: Session = Depends(get_db)):
# #     db_activity_log = db.query(ActivityLog).filter(ActivityLog.log_id == log_id).first()
# #     if db_activity_log is None:
# #         raise HTTPException(status_code=404, detail="Activity log not found")
# #     db.delete(db_activity_log)
# #     db.commit()
# #     return {"message": "Activity log deleted successfully"}

# # Repeat similar CRUD operations for EmissionFactor, Goal, Achievement, Tip, Report

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)





