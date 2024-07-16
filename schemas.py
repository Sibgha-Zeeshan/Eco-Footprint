from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# User schema
class UserBase(BaseModel):
    username: str
    email: str
    profile_info: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    user_id: int

    model_config = ConfigDict(from_attributes=True)

class UserOut(UserBase):
    user_id: int

    model_config = ConfigDict(from_attributes=True)

# ActivityLog schema
class ActivityLogBase(BaseModel):
    user_id: int
    activity_type: str
    activity_value: float
    date: datetime

class ActivityLogCreate(ActivityLogBase):
    pass

class ActivityLogUpdate(ActivityLogBase):
    user_id: Optional[int]
    activity_type: Optional[str]
    activity_value: Optional[float]
    date: Optional[datetime]

class ActivityLog(ActivityLogBase):
    log_id: int

    model_config = ConfigDict(from_attributes=True)

# Emission Factor Schema 
class EmissionFactorBase(BaseModel):
    activity_type: str
    emission_factor: float

class EmissionFactorCreate(EmissionFactorBase):
    pass

class EmissionFactor(EmissionFactorBase):
    factor_id: int

    model_config = ConfigDict(from_attributes=True)

# Goal schemas
class GoalBase(BaseModel):
    user_id: int
    target_reduction: float
    deadline: datetime
    achieved: bool

class GoalCreate(GoalBase):
    pass

class GoalUpdate(GoalBase):
    user_id: Optional[int]
    target_reduction: Optional[float]
    deadline: Optional[datetime]
    achieved: Optional[bool]

class Goal(GoalBase):
    goal_id: int

    model_config = ConfigDict(from_attributes=True)

#Achievemnet
class AchievementBase(BaseModel):
    user_id: int
    achievement_type: str
    date_awarded: datetime

class AchievementCreate(AchievementBase):
    pass

class AchievementOut(AchievementBase):
    achievement_id: int

    model_config = ConfigDict(from_attributes=True)

# Report Schema

class ReportBase(BaseModel):
    user_id: int
    report_data: str
    generated_date: Optional[datetime]

class ReportCreate(ReportBase):
    pass

class Report(ReportBase):
    report_id: int

    model_config = ConfigDict(from_attributes=True)

# Tip Schemas
class TipBase(BaseModel):
    tip_text: str
    category: str
    user_id: int

class TipCreate(TipBase):
    pass

class Tip(TipBase):
    tip_id: int

    class Config:
        orm_mode = True
