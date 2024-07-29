from fastapi import FastAPI
from backend.app.routers import users, activitylog, emissionfactor, goals, achievements, report, tips
from backend.app.database import engine, Base, get_db
import sys
import os
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth, OAuthError
from starlette.requests import Request
from starlette.responses import RedirectResponse
from dotenv import load_dotenv
from fastapi import HTTPException, status, Depends
from starlette.middleware.sessions import SessionMiddleware  # Import SessionMiddleware
import logging
import secrets


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# CORS 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Add SessionMiddleware for session management
# app.add_middleware(SessionMiddleware, secret_key="SEcret1122#$%") 

#Origins of frontend and backend
origins = [
    "http://localhost:5173", 
    "https://accounts.google.com/"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session secret key
SESSION_SECRET_KEY = "12345ooo!"
if not SESSION_SECRET_KEY:
    try:
        SESSION_SECRET_KEY = secrets.token_urlsafe(32)
    except Exception as e:
        logging.error(f"Generated SESSION_SECRET_KEY: {str(e)}")

app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)

oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.environ.get('client_ID'),
    client_secret=os.environ.get('client_secret'),
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri='http://localhost:8000/auth/callback',
    client_kwargs={'scope': 'openid email profile'}
)

@app.get('/auth/login')
async def login(request: Request):
     redirect_uri = request.url_for('auth')
     state = '1234567'
     request.session['state'] = state  # Store the state in the session
     return await oauth.google.authorize_redirect(request, redirect_uri, state = state)

@app.get('/auth/callback')
async def auth(request: Request, db: Session = Depends(get_db)):
    try:
        # Log the state value stored in the session
        stored_state = request.session.get('state')
        logging.debug(f"Stored state: {stored_state}")

        # Retrieve and log the state from the callback URL
        query_params = request.query_params
        received_state = query_params.get('state')
        logging.debug(f"Received state: {received_state}")

        # Check state parameter
        if stored_state != received_state:
            raise OAuthError('mismatching_state', 'State mismatch error.')

        token = await oauth.google.authorize_access_token(request)
        user_info = await oauth.google.parse_id_token(request, token)
    except OAuthError as e:
        logging.error(f"OAuth error: {e.error}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OAuth failed")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    if not user_info:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User information could not be retrieved")

    # Process user information...
    # Redirect user after processing
    return RedirectResponse(url='/')

# Include the routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(activitylog.router, prefix="/api/activity-logs", tags=["activity_logs"]) 
app.include_router(emissionfactor.router, prefix="/emission-factors", tags=["emission-factors"])
app.include_router(goals.router, prefix="/goals", tags=["goals"])
app.include_router(achievements.router, prefix="/achievements", tags=["achievements"])
app.include_router(report.router, prefix="/reports", tags=["reports"])
app.include_router(tips.router, prefix="/tips", tags=["tips"])








@app.get("/")
def read_root():
    return {"message": "Welcome to the EcoFootprint API"}
