from app.models import User, Achievement, ActivityLog, Goal, EmissionFactor, Report as DBReport, Tip
from app.schemas import TipCreate, ReportCreate, AchievementCreate, UserCreate, ActivityLogCreate, ActivityLogUpdate, GoalCreate, GoalUpdate, EmissionFactorCreate
from sqlalchemy.orm import Session
from datetime import datetime, timezone

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
        for key, value in activity_log.model_dump(exclude_unset=True).items():
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

# Business logic and service layer functions
# ------------------- Utility Functions -------------------

def get_user_emissions(db: Session, user_id: int):
    activities = db.query(ActivityLog).filter(ActivityLog.user_id == user_id).all()
    total_emissions = 0
    emission_factors = {
        "car_travel": 0.21,
        "public_transport": 0.1,
        "electricity_usage": 0.5,
        "natural_gas_usage":2.2,
        "waste_generation":0.3,
        "water_usage":  0.001,
        "air_travel":  0.25,
        "food_consumption_meat": 27,
        "food_consumption_vegetables":2,
         "clothing_purchases":14
    }
    
    for activity in activities:
        factor = emission_factors.get(activity.activity_type, 0)
        total_emissions += activity.activity_value * factor
    
    return total_emissions

def generate_emission_report(db: Session, user_id: int):
    total_emissions = get_user_emissions(db, user_id)
    report_data = f"Total emissions for user {user_id}: {total_emissions} kg CO2e"
    report = DBReport(
        user_id=user_id,
        report_data=report_data,
        generated_date=datetime.now(timezone.utc)
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

def generate_tips(db: Session, user_id: int):
    activities = db.query(ActivityLog).filter(ActivityLog.user_id == user_id).all()
    tips = []
    emission_factors = {
        "car_travel": {"factor": 0.21, "benchmark": 100, "tip": "Consider carpooling or using public transportation to reduce emissions.", "category": "transportation"},
        "public_transportation": {"factor": 0.1, "benchmark": 200, "tip": "Check if you can reduce your public transportation usage by combining trips or choosing off-peak times.", "category": "transportation"},
        "electricity_usage": {"factor": 0.475, "benchmark": 500, "tip": "Reduce electricity consumption by using energy-efficient appliances and turning off lights when not in use.", "category": "energy"},
        "natural_gas_usage": {"factor": 2.2, "benchmark": 100, "tip": "Improve home insulation to reduce natural gas usage and lower your heating bills.", "category": "energy"},
        "waste_generation": {"factor": 0.3, "benchmark": 50, "tip": "Recycle and compost to minimize waste and reduce emissions.", "category": "waste"},
        "water_usage": {"factor": 0.001, "benchmark": 10000, "tip": "Reduce water usage by fixing leaks, using water-efficient fixtures, and taking shorter showers.", "category": "water"},
        "air_travel": {"factor": 0.25, "benchmark": 1000, "tip": "Limit air travel where possible and consider alternatives like video conferencing.", "category": "travel"},
        "food_consumption_meat": {"factor": 27, "benchmark": 5, "tip": "Reduce meat consumption and consider plant-based alternatives to lower your carbon footprint.", "category": "food"},
        "food_consumption_vegetables": {"factor": 2, "benchmark": None, "tip": "Continue consuming a variety of vegetables to maintain a low-carbon diet.", "category": "food"},
        "clothing_purchases": {"factor": 14, "benchmark": 5, "tip": "Buy fewer, higher-quality items and consider second-hand clothing to reduce emissions.", "category": "clothing"}
    }
    
    for activity in activities:
        details = emission_factors.get(activity.activity_type)
        if details and activity.activity_value * details['factor'] > details['benchmark']:
            tips.append({"tip_text": details['tip'], "category": details['category']})
    
    return tips

def save_tips(db: Session, user_id: int, tips):
    for tip_info in tips:
        tip = Tip(
            tip_text=tip_info["tip_text"],
            category=tip_info["category"],
            user_id=user_id
        )
        db.add(tip)
    db.commit()


def get_and_generate_tips(db: Session, user_id: int):
    tips = generate_tips(db, user_id)
    save_tips(db, user_id, tips)
    return tips

def provide_tips_to_user(db: Session, user_id: int):
    tips = get_and_generate_tips(db, user_id)
    return tips


def check_goal_achievement(db: Session, user_id: int):
    goals = db.query(Goal).filter(Goal.user_id == user_id).all()
    total_emissions = get_user_emissions(db, user_id)
    achieved_goals = []

    for goal in goals:
        if total_emissions <= goal.target_reduction:
            goal.achieved = True
            achieved_goals.append(goal)
            db.commit()
    
    return achieved_goals