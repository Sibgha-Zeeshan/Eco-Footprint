from app.models import User
from app.schemas import UserCreate
from sqlalchemy.orm import Session


def create_user(db: Session, user: UserCreate):
    try:
        db_user = User(username=user.username, email=user.email, password=user.password, profile_info=user.profile_info)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {
            'status': 'ok',
            'message': 'user created'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }

def get_users(db: Session, skip: int = 0, limit: int = 10):
    try:
        users = db.query(User).offset(skip).limit(limit).all()
        return users
    except Exception as e:
        raise Exception(f"Error retrieving users: {str(e)}")
    
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