import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User
from app.schemas import UserCreate
from app.crud import update_user, delete_user

# Replace 'your_database_url' with your actual database URL
DATABASE_URL = "postgresql+psycopg2://postgres:grepost5566@127.0.0.1:5432/Tracker"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def test_create_user_performance():
    try:
        session = Session()
        start_time = time.time()
        
        # Create operation
        for i in range(1000):
            user = User(username=f'user{i}', email=f'user{i + 1000}@example.com', password='password', profile_info=f'Profile info {i}')
            session.add(user)
        session.commit()
        
        create_time = time.time() - start_time
        print(f"Time taken for creating 500 users: {create_time:.4f} seconds")
        assert create_time < 3  # Adjust the threshold as needed
    
    finally:
        session.close()

def test_read_user_performance():
    try:
        session = Session()
        start_time = time.time()
        
        users = session.query(User).all()
        
        read_time = time.time() - start_time
        print(f"Time taken for reading {len(users)} users: {read_time:.4f} seconds")
        assert read_time < 3  # Adjust the threshold as needed
    
    finally:
        session.close()

def test_update_user_performance():
    try:
        session = Session()
        # Test User update operation performance
        users = session.query(User).all()
        start_time = time.time()
        for i, user in enumerate(users):
            user_data = UserCreate(username=user.username, email=f'updated{i}@example.com', password='newpassword', profile_info='Updated profile')
            update_user(session, user.user_id, user_data)
        session.commit()
        update_time = time.time() - start_time
        print(f"Time taken for updating {len(users)} users: {update_time:.4f} seconds")
        assert update_time < 7  # Adjust the threshold as needed
    except Exception as e:
        session.rollback()
        print(f"Error during update user performance test: {e}")
    finally:
        session.close()

def test_delete_user_performance():
    try:
        session = Session()
        # Test User delete operation performance
        users = session.query(User).all()
        start_time = time.time()
        for user in users:
            delete_user(session, user.user_id)
        session.commit()
        delete_time = time.time() - start_time
        print(f"Time taken for deleting {len(users)} users: {delete_time:.4f} seconds")
        assert delete_time < 5 # Adjust the threshold as needed
    except Exception as e:
        session.rollback()
        print(f"Error during delete user performance test: {e}")
    finally:
        session.close()

if __name__ == '__main__':
    test_create_user_performance()
    test_read_user_performance()
    test_update_user_performance()
    test_delete_user_performance()
