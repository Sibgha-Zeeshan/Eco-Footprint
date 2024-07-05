from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

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

class ActivityLogBase(BaseModel):
    user_id: int
    activity_type: str
    activity_value: float
    date: datetime

class ActivityLog(ActivityLogBase):
    log_id: int

    model_config = ConfigDict(from_attributes=True)

class EmissionFactorBase(BaseModel):
    activity_type: str
    emission_factor: float

class EmissionFactor(EmissionFactorBase):
    factor_id: int

    model_config = ConfigDict(from_attributes=True)

class GoalBase(BaseModel):
    user_id: int
    target_reduction: float
    deadline: datetime
    achieved: bool

class Goal(GoalBase):
    goal_id: int

    model_config = ConfigDict(from_attributes=True)
class AchievementBase(BaseModel):
    user_id: int
    achievement_type: str
    date_awarded: datetime

class Achievement(AchievementBase):
    achievement_id: int

    model_config = ConfigDict(from_attributes=True)
class TipBase(BaseModel):
    tip_text: str
    category: str
    user_id: int

class Tip(TipBase):
    tip_id: int

    model_config = ConfigDict(from_attributes=True)

class ReportBase(BaseModel):
    user_id: int
    report_data: str
    generated_date: datetime

class Report(ReportBase):
    report_id: int

    model_config = ConfigDict(from_attributes=True)
