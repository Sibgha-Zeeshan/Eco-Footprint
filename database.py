# ----------------Connection point --------------------
import os
from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# This will show all deprecation warnings, helping you identify other changes needed for compatibility with SQLAlchemy 2.0.
os.environ['SQLALCHEMY_WARN_20'] = '1'



Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    profile_info = Column(String)

class ActivityLog(Base):
    __tablename__ = 'activity_logs'
    log_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    activity_type = Column(String, nullable=False)
    activity_value = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    user = relationship("User")

class EmissionFactor(Base):
    __tablename__ = 'emission_factors'
    factor_id = Column(Integer, primary_key=True)
    activity_type = Column(String, nullable=False)
    emission_factor = Column(Float, nullable=False)

class Goal(Base):
    __tablename__ = 'goals'
    goal_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    target_reduction = Column(Float, nullable=False)
    deadline = Column(DateTime, nullable=False)
    achieved = Column(Boolean, nullable=False)
    user = relationship("User")

class Achievement(Base):
    __tablename__ = 'achievements'
    achievement_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    achievement_type = Column(String, nullable=False)
    date_awarded = Column(DateTime, nullable=False)
    user = relationship("User")

class Tip(Base):
    __tablename__ = 'tips'
    tip_id = Column(Integer, primary_key=True)
    tip_text = Column(String, nullable=False)
    category = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    user = relationship("User")

class Report(Base):
    __tablename__ = 'reports'
    report_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    report_data = Column(String, nullable=False)
    generated_date = Column(DateTime, nullable=False)
    user = relationship("User")

db_path = os.path.join(os.getcwd(), 'Tracker.db')
print(f"Database will be created at: {db_path}")

engine = create_engine(r"postgresql+psycopg2://postgres:grepost5566@127.0.0.1:5432/Tracker")
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

print("Databases will be created successfully")