from app.models import User, Achievement, ActivityLog, Goal, EmissionFactor, Report as DBReport, Tip
from app.schemas import TipCreate, ReportCreate, AchievementCreate, UserCreate, ActivityLogCreate, ActivityLogUpdate, GoalCreate, GoalUpdate, EmissionFactorCreate
from sqlalchemy.orm import Session

# -------------------------------------------USER----------------------------------------------------------
def get_users(db: Session, skip: int = 0, limit: int = 10):
    try:
        users = db.query(User).offset(skip).limit(limit).all()
        return users
    except Exception as e:
        raise Exception(f"Error retrieving users: {str(e)}")
    
def create_user(db: Session, user: UserCreate):
    try:
        db_user = User(username=user.username, email=user.email, password=user.password, profile_info=user.profile_info)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"status": "success", "user": db_user}
    except Exception as e:
        db.rollback()
        raise Exception(f"Error creating user: {str(e)}")

def get_user(db: Session, user_id: int):
    try:
        return db.query(User).filter(User.user_id == user_id).first()
    except Exception as e:
        raise Exception(f"Error retrieving user: {str(e)}")

def update_user(db: Session, user_id: int, user: UserCreate):
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        if db_user:
            db_user.username = user.username
            db_user.email = user.email
            db_user.password = user.password
            db_user.profile_info = user.profile_info
            db.commit()
            db.refresh(db_user)
        else:
            raise Exception("User not found")
        return db_user
    except Exception as e:
        db.rollback()
        raise Exception(f"Error updating user: {str(e)}")

def delete_user(db: Session, user_id: int):
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        if db_user:
            db.delete(db_user)
            db.commit()
        else:
            raise Exception("User not found")
        return db_user
    except Exception as e:
        db.rollback()
        raise Exception(f"Error deleting user: {str(e)}")
    
# ------------------------------------------- ACTIVITY LOG ----------------------------------------------------------
def create_activity_log(db: Session, activity_log: ActivityLogCreate):
    db_activity_log = ActivityLog(
        user_id=activity_log.user_id,
        activity_type=activity_log.activity_type,
        activity_value=activity_log.activity_value,
        date=activity_log.date
    )
    db.add(db_activity_log)
    db.commit()
    db.refresh(db_activity_log)
    return db_activity_log

def get_activity_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ActivityLog).offset(skip).limit(limit).all()

def get_activity_log(db: Session, log_id: int):
    return db.query(ActivityLog).filter(ActivityLog.log_id == log_id).first()

def update_activity_log(db: Session, log_id: int, activity_log: ActivityLogUpdate):
    db_activity_log = db.query(ActivityLog).filter(ActivityLog.log_id == log_id).first()
    if db_activity_log:
        for key, value in activity_log.dict(exclude_unset=True).items():
            setattr(db_activity_log, key, value)
        db.commit()
        db.refresh(db_activity_log)
    return db_activity_log

def delete_activity_log(db: Session, log_id: int):
    db_activity_log = db.query(ActivityLog).filter(ActivityLog.log_id == log_id).first()
    if db_activity_log:
        db.delete(db_activity_log)
        db.commit()
    return db_activity_log
# ------------------------------------------- EMISSION FACTOR ----------------------------------------------------------
def create_emission_factor(db: Session, emission_factor: EmissionFactorCreate):
    db_emission_factor = EmissionFactor(**emission_factor.model_dump())
    db.add(db_emission_factor)
    db.commit()
    db.refresh(db_emission_factor)
    return db_emission_factor

def get_emission_factor(db: Session, factor_id: int):
    return db.query(EmissionFactor).filter(EmissionFactor.factor_id == factor_id).first()

def get_emission_factors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(EmissionFactor).offset(skip).limit(limit).all()

def delete_emission_factor(db: Session, factor_id: int):
    db_emission_factor = db.query(EmissionFactor).filter(EmissionFactor.factor_id == factor_id).first()
    if db_emission_factor:
        db.delete(db_emission_factor)
        db.commit()
    return db_emission_factor
# ------------------------------------------- GOAL ----------------------------------------------------------
def create_goal(db: Session, goal: GoalCreate):
    db_goal = Goal(
        user_id=goal.user_id,
        target_reduction=goal.target_reduction,
        deadline=goal.deadline,
        achieved=goal.achieved
    )
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal


def get_goals(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Goal).offset(skip).limit(limit).all()


def get_goal(db: Session, goal_id: int):
    return db.query(Goal).filter(Goal.goal_id == goal_id).first()


def update_goal(db: Session, goal_id: int, goal: GoalUpdate):
    db_goal = db.query(Goal).filter(Goal.goal_id == goal_id).first()
    if db_goal:
        for key, value in goal.model_dump(exclude_unset=True).items():
            setattr(db_goal, key, value)
        db.commit()
        db.refresh(db_goal)
    return db_goal


def delete_goal(db: Session, goal_id: int):
    db_goal = db.query(Goal).filter(Goal.goal_id == goal_id).first()
    if db_goal:
        db.delete(db_goal)
        db.commit()
    return db_goal

# ------------------------------------------- ACHIEVEMENT ----------------------------------------------------
def get_achievements(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Achievement).offset(skip).limit(limit).all()

def create_achievement(db: Session, achievement: AchievementCreate):
    db_achievement = Achievement(
        user_id=achievement.user_id,
        achievement_type=achievement.achievement_type,
        date_awarded=achievement.date_awarded
    )
    db.add(db_achievement)
    db.commit()
    db.refresh(db_achievement)
    return db_achievement

def get_achievement(db: Session, achievement_id: int):
    return db.query(Achievement).filter(Achievement.achievement_id == achievement_id).first()

def update_achievement(db: Session, achievement_id: int, achievement: AchievementCreate):
    db_achievement = db.query(Achievement).filter(Achievement.achievement_id == achievement_id).first()
    if db_achievement:
        db_achievement.user_id = achievement.user_id
        db_achievement.achievement_type = achievement.achievement_type
        db_achievement.date_awarded = achievement.date_awarded
        db.commit()
        db.refresh(db_achievement)
    return db_achievement

def delete_achievement(db: Session, achievement_id: int):
    db_achievement = db.query(Achievement).filter(Achievement.achievement_id == achievement_id).first()
    if db_achievement:
        db.delete(db_achievement)
        db.commit()
    return db_achievement

# ------------------------------------------- REPORT ---------------------------------------------------------
def get_report(db: Session, report_id: int):
    return db.query(DBReport).filter(DBReport.report_id == report_id).first()

def get_reports(db: Session, skip: int = 0, limit: int = 10):
    return db.query(DBReport).offset(skip).limit(limit).all()


def create_report(db: Session, report: ReportCreate):
    db_report = DBReport(
        user_id=report.user_id,
        report_data=report.report_data,
        generated_date=report.generated_date
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


def update_report(db: Session, report_id: int, report: ReportCreate):
    db_report = db.query(DBReport).filter(DBReport.report_id == report_id).first()
    if db_report:
        db_report.user_id = report.user_id
        db_report.report_data = report.report_data
        db_report.generated_date = report.generated_date
        db.commit()
        db.refresh(db_report)
    return db_report


def delete_report(db: Session, report_id: int):
    db_report = db.query(DBReport).filter(DBReport.report_id == report_id).first()
    if db_report:
        db.delete(db_report)
        db.commit()
    return db_report

# ------------------------------------------- TIP ----------------------------------------------------------
def get_tip(db: Session, tip_id: int):
    return db.query(Tip).filter(Tip.tip_id == tip_id).first()

def get_tips(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Tip).offset(skip).limit(limit).all()

def create_tip(db: Session, tip: TipCreate):
    db_tip = Tip(
        tip_text=tip.tip_text,
        category=tip.category,
        user_id=tip.user_id
    )
    db.add(db_tip)
    db.commit()
    db.refresh(db_tip)
    return db_tip

def update_tip(db: Session, tip_id: int, tip: TipCreate):
    db_tip = db.query(Tip).filter(Tip.tip_id == tip_id).first()
    if db_tip:
        db_tip.tip_text = tip.tip_text
        db_tip.category = tip.category
        db_tip.user_id = tip.user_id
        db.commit()
        db.refresh(db_tip)
    return db_tip

def delete_tip(db: Session, tip_id: int):
    db_tip = db.query(Tip).filter(Tip.tip_id == tip_id).first()
    if db_tip:
        db.delete(db_tip)
        db.commit()
    return db_tip
