# coding: utf-8
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class EmissionFactor(Base):
    __tablename__ = 'emission_factors'

    factor_id = Column(Integer, primary_key=True)
    activity_type = Column(String, nullable=False)
    emission_factor = Column(Float(53), nullable=False)


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    profile_info = Column(String)


class Achievement(Base):
    __tablename__ = 'achievements'

    achievement_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.user_id'))
    achievement_type = Column(String, nullable=False)
    date_awarded = Column(DateTime, nullable=False)

    user = relationship('User')


class ActivityLog(Base):
    __tablename__ = 'activity_logs'

    log_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.user_id'))
    activity_type = Column(String, nullable=False)
    activity_value = Column(Float(53), nullable=False)
    date = Column(DateTime, nullable=False)

    user = relationship('User')


class Goal(Base):
    __tablename__ = 'goals'

    goal_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.user_id'))
    target_reduction = Column(Float(53), nullable=False)
    deadline = Column(DateTime, nullable=False)
    achieved = Column(Boolean, nullable=False)

    user = relationship('User')


class Report(Base):
    __tablename__ = 'reports'

    report_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.user_id'))
    report_data = Column(String, nullable=False)
    generated_date = Column(DateTime, nullable=False)

    user = relationship('User')


class Tip(Base):
    __tablename__ = 'tips'

    tip_id = Column(Integer, primary_key=True)
    tip_text = Column(String, nullable=False)
    category = Column(String, nullable=False)
    user_id = Column(ForeignKey('users.user_id'))

    user = relationship('User')
