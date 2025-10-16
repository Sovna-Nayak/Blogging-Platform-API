from sqlalchemy.orm import Session
import Auth.models, Auth.schemas
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_user_by_username(db: Session, username: str):
    return db.query(Auth.models.User).filter(Auth.models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(Auth.models.User).filter(Auth.models.User.email == email).first()


def create_user(db: Session, user: Auth.schemas.UserCreate):
    hashed = pwd_context.hash(user.password)
    db_user = Auth.models.User(username=user.username, email=user.email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)