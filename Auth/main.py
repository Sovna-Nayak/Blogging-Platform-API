
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer,HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt

import Auth.models, Auth.schemas, Auth.crud, Auth.deps

Auth.models.Base.metadata.create_all(bind=Auth.deps.engine)

router = APIRouter()

# ---------------- JWT Config ----------------
SECRET = 'supersecret'
ALGORITHM = 'HS256'

# OAuth2 scheme for Swagger UI
security = HTTPBearer() 

# ---------------- Auth Helpers ----------------

def create_access_token(data: dict, expires_minutes: int = 60):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(Auth.deps.get_db)
):
    """
    Expects header: Authorization: Bearer <token>
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = Auth.crud.get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ------------------ Routes ------------------

@router.post('/signup', response_model=Auth.schemas.UserOut)
def signup(user: Auth.schemas.UserCreate, db: Session = Depends(Auth.deps.get_db)):
    if Auth.crud.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail='Username already exists')
    if Auth.crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail='Email already in use')
    return Auth.crud.create_user(db, user)


@router.post('/login', response_model=Auth.schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(Auth.deps.get_db)):
    user = Auth.crud.get_user_by_username(db, form_data.username)
    if not user or not Auth.crud.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Invalid credentials')

    access_token = create_access_token({"sub": user.username, "email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# ------------------ New Authorize Route ------------------


@router.get("/me")
def read_me(current_user = Depends(get_current_user)):
    return {"username": current_user.username, "email": current_user.email}
