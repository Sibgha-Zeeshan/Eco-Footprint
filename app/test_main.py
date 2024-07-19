import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import User, Achievement, ActivityLog, Goal, EmissionFactor, Report, Tip
from datetime import datetime, timezone, timedelta
from app.crud import (
    get_user_emissions, generate_emission_report, generate_tips,
    save_tips, get_and_generate_tips, provide_tips_to_user, check_goal_achievement
)

# Use the test PostgreSQL database URL
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:grepost5566@127.0.0.1:5432/testdb"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session local class
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup():
    # Create the test database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop the test database tables
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function", autouse=True)
def clear_data():
    # Clear the tables before each test
    db = TestingSessionLocal()
    db.query(Tip).delete()
    db.query(Report).delete()
    db.query(EmissionFactor).delete()
    db.query(Goal).delete()
    db.query(Achievement).delete()
    db.query(ActivityLog).delete()
    db.query(User).delete()
    db.commit()
    db.close()

# User Fixtures and Tests
@pytest.fixture
def test_user_data():
    return {"username": "testuser", "email": "test@example.com", "password": "password123", "profile_info": "Test Profile"}

@pytest.fixture
def create_test_user(test_user_data):
    db = TestingSessionLocal()
    user = User(**test_user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user
    db.close()

def test_create_user(test_user_data):
    response = client.post("/users/", json=test_user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert "user" in data  # Check if 'user' key exists in the response
    user_data = data["user"]
    assert user_data["username"] == test_user_data["username"]
    assert user_data["email"] == test_user_data["email"]

def test_read_users(create_test_user):
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["username"] == create_test_user.username
    assert data[0]["email"] == create_test_user.email

def test_read_user(create_test_user):
    user_id = create_test_user.user_id
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == create_test_user.username
    assert data["email"] == create_test_user.email

def test_update_user(create_test_user):
    user_id = create_test_user.user_id
    updated_data = {"username": "updateduser", "email": "updated@example.com", "password": "newpassword123", "profile_info": "Updated Profile"}
    response = client.put(f"/users/{user_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == updated_data["username"]
    assert data["email"] == updated_data["email"]

def test_delete_user(create_test_user):
    user_id = create_test_user.user_id
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404
# Achievement Fixtures and Tests
@pytest.fixture
def test_achievement_data(create_test_user):
    return {
        "user_id": create_test_user.user_id,
        "achievement_type": "Test Achievement",
        "date_awarded": "2024-07-05T00:00:00Z"
    }

@pytest.fixture
def create_test_achievement(test_achievement_data):
    db = TestingSessionLocal()
    achievement = Achievement(**test_achievement_data)
    db.add(achievement)
    db.commit()
    db.refresh(achievement)
    yield achievement
    db.close()

def test_create_achievement(test_user_data):
    # Create the user needed for the achievement
    db = TestingSessionLocal()
    user = User(**test_user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    achievement_data = {
        "user_id": user.user_id,
        "achievement_type": "Test Achievement",
        "date_awarded": "2024-07-05T00:00:00Z"
    }
    db.close()

    response = client.post("/achievements/", json=achievement_data)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert "achievement" in data  # Check if 'achievement' key exists in the response
    achievement_response_data = data["achievement"]
    assert achievement_response_data["achievement_type"] == achievement_data["achievement_type"]
    assert achievement_response_data["user_id"] == achievement_data["user_id"]

def test_read_achievements(create_test_achievement):
    response = client.get("/achievements/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["achievements"]) > 0
    achievement_data = data["achievements"][0]
    assert achievement_data["achievement_type"] == create_test_achievement.achievement_type
    assert achievement_data["user_id"] == create_test_achievement.user_id

def test_read_achievement(create_test_achievement):
    achievement_id = create_test_achievement.achievement_id
    response = client.get(f"/achievements/{achievement_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    achievement_data = data["achievement"]
    assert achievement_data["achievement_type"] == create_test_achievement.achievement_type
    assert achievement_data["user_id"] == create_test_achievement.user_id


def test_update_achievement(create_test_achievement):
    achievement_id = create_test_achievement.achievement_id
    updated_data = {
        "user_id": create_test_achievement.user_id,
        "achievement_type": "Updated Achievement",
        "date_awarded": "2024-07-06T00:00:00Z"
    }
    response = client.put(f"/achievements/{achievement_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    achievement_data = data["achievement"]
    assert achievement_data["achievement_type"] == updated_data["achievement_type"]

    # Convert both dates to UTC
    actual_date = datetime.fromisoformat(achievement_data["date_awarded"].replace("Z", "+00:00")).astimezone(timezone.utc)
    expected_date = datetime.fromisoformat(updated_data["date_awarded"].replace("Z", "+00:00")).astimezone(timezone.utc)
    assert actual_date == expected_date

# Activity Log Unit Tests --------------------------------------------------------------------------
@pytest.fixture
def test_activity_log_data(create_test_user):
    return {
        "user_id": create_test_user.user_id,
        "activity_type": "running",
        "activity_value": 30.0,
        "date": "2024-07-15T00:00:00Z"
    }

@pytest.fixture
def create_test_activity_log(test_activity_log_data):
    db = TestingSessionLocal()
    activity_log = ActivityLog(**test_activity_log_data)
    db.add(activity_log)
    db.commit()
    db.refresh(activity_log)
    yield activity_log
    db.close()

def test_create_activity_log(test_activity_log_data):
    response = client.post("/activity-logs/", json=test_activity_log_data)  # Corrected prefix
    assert response.status_code == 201
    data = response.json()
    assert data["activity_type"] == test_activity_log_data["activity_type"]
    assert data["activity_value"] == test_activity_log_data["activity_value"]
    
    # Convert both dates to UTC for comparison
    actual_date = datetime.fromisoformat(data["date"].replace("Z", "+00:00")).astimezone(timezone.utc)
    expected_date = datetime.fromisoformat(test_activity_log_data["date"].replace("Z", "+00:00")).astimezone(timezone.utc)
    assert actual_date == expected_date

def test_read_activity_logs(create_test_activity_log):
    response = client.get("/activity-logs/")  # Corrected prefix
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["activity_type"] == create_test_activity_log.activity_type
    assert data[0]["activity_value"] == create_test_activity_log.activity_value

def test_read_activity_log(create_test_activity_log):
    activity_log_id = create_test_activity_log.log_id
    response = client.get(f"/activity-logs/{activity_log_id}")  # Corrected prefix
    assert response.status_code == 200
    data = response.json()
    assert data["activity_type"] == create_test_activity_log.activity_type
    assert data["activity_value"] == create_test_activity_log.activity_value

def test_update_activity_log(create_test_activity_log):
    activity_log_id = create_test_activity_log.log_id
    updated_data = {
        "user_id": create_test_activity_log.user_id,
        "activity_type": "cycling",
        "activity_value": 45.0,
        "date": "2024-07-16T00:00:00Z"
    }
    response = client.put(f"/activity-logs/{activity_log_id}", json=updated_data)  # Corrected prefix
    assert response.status_code == 200
    data = response.json()
    assert data["activity_type"] == updated_data["activity_type"]
    assert data["activity_value"] == updated_data["activity_value"]

def test_delete_activity_log(create_test_activity_log):
    activity_log_id = create_test_activity_log.log_id
    response = client.delete(f"/activity-logs/{activity_log_id}")  # Corrected prefix
    assert response.status_code == 200
    response = client.get(f"/activity-logs/{activity_log_id}")  # Corrected prefix
    assert response.status_code == 404

# Goal Unit Tests ---------------------------------------------------------------------------------
@pytest.fixture
def test_goal_data(create_test_user):
    return {
        "user_id": create_test_user.user_id,
        "target_reduction": 20.0,
        "deadline": "2024-12-31T23:59:59Z",
        "achieved": False
    }

@pytest.fixture
def create_test_goal(test_goal_data):
    db = TestingSessionLocal()
    goal = Goal(**test_goal_data)
    db.add(goal)
    db.commit()
    db.refresh(goal)
    yield goal
    db.close()

def test_create_goal(test_goal_data):
    response = client.post("/goals/", json=test_goal_data)
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == test_goal_data["user_id"]
    assert data["target_reduction"] == test_goal_data["target_reduction"]
    assert data["achieved"] == test_goal_data["achieved"]

    # Convert both dates to UTC for comparison
    actual_date = datetime.fromisoformat(data["deadline"].replace("Z", "+00:00")).astimezone(timezone.utc)
    expected_date = datetime.fromisoformat(test_goal_data["deadline"].replace("Z", "+00:00")).astimezone(timezone.utc)
    assert actual_date == expected_date

def test_read_goals(create_test_goal):
    response = client.get("/goals/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["user_id"] == create_test_goal.user_id
    assert data[0]["target_reduction"] == create_test_goal.target_reduction
    assert data[0]["achieved"] == create_test_goal.achieved

def test_read_goal(create_test_goal):
    goal_id = create_test_goal.goal_id
    response = client.get(f"/goals/{goal_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == create_test_goal.user_id
    assert data["target_reduction"] == create_test_goal.target_reduction
    assert data["achieved"] == create_test_goal.achieved

def test_update_goal(create_test_goal):
    goal_id = create_test_goal.goal_id
    updated_data = {
        "user_id": create_test_goal.user_id,
        "target_reduction": 25.0,
        "deadline": "2025-06-30T23:59:59Z",
        "achieved": True
    }
    response = client.put(f"/goals/{goal_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == updated_data["user_id"]
    assert data["target_reduction"] == updated_data["target_reduction"]
    assert data["achieved"] == updated_data["achieved"]

    # Convert both dates to UTC for comparison
    actual_date = datetime.fromisoformat(data["deadline"].replace("Z", "+00:00")).astimezone(timezone.utc)
    expected_date = datetime.fromisoformat(updated_data["deadline"].replace("Z", "+00:00")).astimezone(timezone.utc)
    assert actual_date == expected_date

def test_delete_goal(create_test_goal):
    goal_id = create_test_goal.goal_id
    response = client.delete(f"/goals/{goal_id}")
    assert response.status_code == 200
    # Check if the goal is really deleted by attempting to fetch it again
    response = client.get(f"/goals/{goal_id}")
    assert response.status_code == 404

#  Test Functions for Emission Factor
@pytest.fixture
def test_emission_factor_data():
    return {
        "activity_type": "driving",
        "emission_factor": 0.21
    }

def test_create_emission_factor(test_emission_factor_data):
    response = client.post("/emission-factors/", json=test_emission_factor_data)
    print(response.json())  # Print the detailed error message
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["activity_type"] == test_emission_factor_data["activity_type"]
    assert data["emission_factor"] == test_emission_factor_data["emission_factor"]

def test_read_emission_factors(test_emission_factor_data):
    client.post("/emission-factors/", json=test_emission_factor_data)
    response = client.get("/emission-factors/")
    print(response.json())  # Print the detailed error message
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) > 0
    assert data[0]["activity_type"] == test_emission_factor_data["activity_type"]
    assert data[0]["emission_factor"] == test_emission_factor_data["emission_factor"]

def test_read_emission_factor(test_emission_factor_data):
    response = client.post("/emission-factors/", json=test_emission_factor_data)
    assert response.status_code == 201, response.text
    factor_id = response.json()["factor_id"]
    response = client.get(f"/emission-factors/{factor_id}")
    print(response.json())  # Print the detailed error message
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["activity_type"] == test_emission_factor_data["activity_type"]
    assert data["emission_factor"] == test_emission_factor_data["emission_factor"]

def test_delete_emission_factor(test_emission_factor_data):
    response = client.post("/emission-factors/", json=test_emission_factor_data)
    assert response.status_code == 201, response.text
    factor_id = response.json()["factor_id"]
    response = client.delete(f"/emission-factors/{factor_id}")
    print(response.json())  # Print the detailed error message
    assert response.status_code == 200, response.text
    response = client.get(f"/emission-factors/{factor_id}")
    assert response.status_code == 404, response.text

# Test Functions for Report
@pytest.fixture
def test_report_data(create_test_user):
    return {
        "user_id": create_test_user.user_id,
        "report_data": "Sample report data",
        "generated_date": "2024-07-15T00:00:00Z"
    }

@pytest.fixture
def create_test_report(test_report_data):
    db = TestingSessionLocal()
    report = Report(**test_report_data)
    db.add(report)
    db.commit()
    db.refresh(report)
    yield report
    db.close()

# Unit Tests
def test_create_report(test_report_data):
    response = client.post("/reports/", json=test_report_data)
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == test_report_data["user_id"]
    assert data["report_data"] == test_report_data["report_data"]

    # Convert both dates to UTC for comparison
    actual_date = datetime.fromisoformat(data["generated_date"].replace("Z", "+00:00")).astimezone(timezone.utc)
    expected_date = datetime.fromisoformat(test_report_data["generated_date"].replace("Z", "+00:00")).astimezone(timezone.utc)
    assert actual_date == expected_date

def test_read_reports(create_test_report):
    response = client.get("/reports/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["user_id"] == create_test_report.user_id
    assert data[0]["report_data"] == create_test_report.report_data

def test_read_report(create_test_report):
    report_id = create_test_report.report_id
    response = client.get(f"/reports/{report_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == create_test_report.user_id
    assert data["report_data"] == create_test_report.report_data

def test_update_report(create_test_report):
    report_id = create_test_report.report_id
    updated_data = {
        "user_id": create_test_report.user_id,
        "report_data": "Updated report data",
        "generated_date": "2025-06-30T23:59:59Z"
    }
    response = client.put(f"/reports/{report_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == updated_data["user_id"]
    assert data["report_data"] == updated_data["report_data"]

    # Convert both dates to UTC for comparison
    actual_date = datetime.fromisoformat(data["generated_date"].replace("Z", "+00:00")).astimezone(timezone.utc)
    expected_date = datetime.fromisoformat(updated_data["generated_date"].replace("Z", "+00:00")).astimezone(timezone.utc)
    assert actual_date == expected_date

def test_delete_report(create_test_report):
    report_id = create_test_report.report_id
    response = client.delete(f"/reports/{report_id}")
    assert response.status_code == 200
    # Check if the report is really deleted by attempting to fetch it again
    response = client.get(f"/reports/{report_id}")
    assert response.status_code == 404

# Test Functions for Tip
@pytest.fixture
def test_tip_data(create_test_user):
    return {
        "tip_text": "Sample tip text",
        "category": "General",
        "user_id": create_test_user.user_id
    }

@pytest.fixture
def create_test_tip(test_tip_data):
    db = TestingSessionLocal()
    tip = Tip(**test_tip_data)
    db.add(tip)
    db.commit()
    db.refresh(tip)
    yield tip
    db.close()

# Unit Tests
def test_create_tip(test_tip_data):
    response = client.post("/tips/", json=test_tip_data)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    tip_data = data["tip"]
    assert tip_data["tip_text"] == test_tip_data["tip_text"]
    assert tip_data["category"] == test_tip_data["category"]
    assert tip_data["user_id"] == test_tip_data["user_id"]

def test_read_tips(create_test_tip):
    response = client.get("/tips/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["tip_text"] == create_test_tip.tip_text
    assert data[0]["category"] == create_test_tip.category
    assert data[0]["user_id"] == create_test_tip.user_id

def test_read_tip(create_test_tip):
    tip_id = create_test_tip.tip_id
    response = client.get(f"/tips/{tip_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["tip_text"] == create_test_tip.tip_text
    assert data["category"] == create_test_tip.category
    assert data["user_id"] == create_test_tip.user_id

def test_update_tip(create_test_tip):
    tip_id = create_test_tip.tip_id
    updated_data = {
        "tip_text": "Updated tip text",
        "category": "Updated Category",
        "user_id": create_test_tip.user_id
    }
    response = client.put(f"/tips/{tip_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["tip_text"] == updated_data["tip_text"]
    assert data["category"] == updated_data["category"]
    assert data["user_id"] == updated_data["user_id"]

def test_delete_tip(create_test_tip):
    tip_id = create_test_tip.tip_id
    response = client.delete(f"/tips/{tip_id}")
    assert response.status_code == 204  # Expecting 204 status code for deletion
    # Check if the tip is really deleted by attempting to fetch it again
    response = client.get(f"/tips/{tip_id}")
    assert response.status_code == 404

#  Additional unit tests


@pytest.fixture
def create_activity_logs(create_test_user):
    db = TestingSessionLocal()
    user = create_test_user
    db.add(ActivityLog(user_id=user.user_id, activity_type="car_travel", activity_value=50, date=datetime.now(timezone.utc)))
    db.add(ActivityLog(user_id=user.user_id, activity_type="electricity_usage", activity_value=100, date=datetime.now(timezone.utc)))
    db.commit()
    yield db

@pytest.fixture
def create_goal_and_activities(create_test_user):
    db = TestingSessionLocal()
    user = create_test_user
    db.add(Goal(user_id=user.user_id, target_reduction=500, deadline=datetime.now(timezone.utc) + timedelta(days=30), achieved=False))
    db.add(ActivityLog(user_id=user.user_id, activity_type="car_travel", activity_value=50, date=datetime.now(timezone.utc)))
    db.add(ActivityLog(user_id=user.user_id, activity_type="electricity_usage", activity_value=100, date=datetime.now(timezone.utc)))
    db.commit()
    yield db

def test_get_user_emissions(create_test_user, create_activity_logs):
    user = create_test_user
    db = create_activity_logs

    emissions = get_user_emissions(db, user.user_id)
    assert isinstance(emissions, float)
    assert emissions >= 0

def test_generate_emission_report(create_test_user, create_activity_logs):
    user = create_test_user
    db = create_activity_logs

    report = generate_emission_report(db, user.user_id)
    assert report.user_id == user.user_id
    assert "Total emissions for user" in report.report_data
    assert isinstance(report.generated_date, datetime)

def test_generate_tips(create_test_user, create_activity_logs):
    user = create_test_user
    db = create_activity_logs

    tips = generate_tips(db, user.user_id)
    assert isinstance(tips, list)
    assert all(isinstance(tip, dict) for tip in tips)  # Tips should now be dicts
    assert all("tip_text" in tip and "category" in tip for tip in tips)

def test_save_tips(create_test_user):
    user = create_test_user
    db = TestingSessionLocal()
    tips = [
        {"tip_text": "Consider carpooling or using public transportation to reduce emissions.", "category": "transportation"}
    ]
    save_tips(db, user.user_id, tips)
    saved_tips = db.query(Tip).filter(Tip.user_id == user.user_id).all()
    assert len(saved_tips) == len(tips)
    assert saved_tips[0].tip_text == tips[0]["tip_text"]
    assert saved_tips[0].category == tips[0]["category"]
    db.close()

def test_get_and_generate_tips(create_test_user):
    user = create_test_user
    db = TestingSessionLocal()

    tips = get_and_generate_tips(db, user.user_id)
    assert isinstance(tips, list)
    assert all(isinstance(tip, str) for tip in tips)

def test_provide_tips_to_user(create_test_user):
    user = create_test_user
    db = TestingSessionLocal()

    tips = provide_tips_to_user(db, user.user_id)
    assert isinstance(tips, list)
    assert all(isinstance(tip, str) for tip in tips)

def test_check_goal_achievement(create_test_user, create_goal_and_activities):
    user = create_test_user
    db = create_goal_and_activities

    achieved_goals = check_goal_achievement(db, user.user_id)
    assert isinstance(achieved_goals, list)
    assert all(goal.achieved for goal in achieved_goals)

# Integration tests
def test_get_user_emissions_endpoint(create_test_user):
    user = create_test_user

    response = client.get(f"/users/{user.user_id}/emissions")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, float)
    assert data >= 0

def test_generate_emission_report_endpoint(create_test_user):
    user = create_test_user

    response = client.post(f"/users/{user.user_id}/emission_report")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user.user_id
    assert "Total emissions for user" in data["report_data"]
    assert "generated_date" in data

def test_generate_tips_endpoint(create_test_user):
    user = create_test_user

    response = client.get(f"/users/{user.user_id}/tips")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:  # Check if data is not empty
        assert all(isinstance(tip, dict) for tip in data)  # Assuming tips are returned as list of dicts
        assert "tip_text" in data[0]  # Check if the expected fields are present

def test_check_goal_achievement_endpoint(create_test_user):
    user = create_test_user

    response = client.get(f"/users/{user.user_id}/goal_achievement")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all(goal["achieved"] for goal in data)



