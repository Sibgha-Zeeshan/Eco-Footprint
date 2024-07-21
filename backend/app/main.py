from fastapi import FastAPI
from backend.app.routers import users, activitylog, emissionfactor, goals, achievements, report, tips
from backend.app.database import engine, Base
import sys
import os

# 
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# CORS 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

#Origins of frontend and backend
origins = [
    #URL of frontend
    #domain of backend from ngrok
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include the routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(activitylog.router, prefix="/activity-logs", tags=["activity_logs"]) 
app.include_router(emissionfactor.router, prefix="/emission-factors", tags=["emission-factors"])
app.include_router(goals.router, prefix="/goals", tags=["goals"])
app.include_router(achievements.router, prefix="/achievements", tags=["achievements"])
app.include_router(report.router, prefix="/reports", tags=["reports"])
app.include_router(tips.router, prefix="/tips", tags=["tips"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the EcoFootprint API"}
