
# from fastapi import FastAPI, Depends, HTTPException, Header, Body,APIRouter
# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from jose import jwt, JWTError
# from typing import List
# from pydantic import BaseModel
# from fastapi.security import OAuth2PasswordBearer
# from Auth.main import get_current_user
# from Auth.models import User

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  # your Auth login route


# import Post_Service.models, Post_Service.schemas

# # ---------------- Database ----------------
# DATABASE_URL = "postgresql://postgres:nayak@localhost:5432/abc"
# SECRET = "secret"
# ALGORITHM = "HS256"

# # Corrected: remove `connect_args` for PostgreSQL
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Post_Service.models.Base.metadata.create_all(bind=engine)

# router = APIRouter()

# # ---------------- DB Dependency ----------------
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # ---------------- JWT Verification ----------------
# # def verify_token(authorization: str = Header(...)):
# #     if not authorization.startswith("Bearer "):
# #         raise HTTPException(status_code=401, detail="Invalid authorization header")
# #     token = authorization.split(" ")[1]
# #     try:
# #         payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
# #         return payload.get("username")
# #     except JWTError:
# #         raise HTTPException(status_code=401, detail="Invalid token")
# def verify_token(authorization: str = Header(...), db: Session = Depends(get_db)):
#     if not authorization.startswith("Bearer "):
#         raise HTTPException(status_code=401, detail="Invalid authorization header")
#     token = authorization.split(" ")[1]
#     try:
#         payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
#         username = payload.get("username")
#         if not username:
#             raise HTTPException(status_code=401, detail="Invalid token")
#         # Optionally check if user exists
#         user = get_current_user(db, username)
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
#         return username  # <-- only the string, not the full User object
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")


# # ---------------- Auth Post_Service.Models ----------------
# class AuthRequest(BaseModel):
#     username: str

# class AuthResponse(BaseModel):
#     access_token: str

# # ---------------- Auth Endpoint ----------------
# def get_current_username(user: User = Depends(get_current_user)):
#     return user.username

# @router.post("/authorize", response_model=AuthResponse)
# def authorize(auth: AuthRequest):
#     if not auth.username:
#         raise HTTPException(status_code=400, detail="Username required")
#     token = jwt.encode({"username": auth.username}, SECRET, algorithm=ALGORITHM)
#     return {"access_token": token}

# # ---------------- Post Endpoints ----------------

# @router.get("/posts/", response_model=List[Post_Service.schemas.PostOut])
# def get_posts(db: Session = Depends(get_db)):
#     return db.query(Post_Service.models.Post).all()

# @router.get("/posts/{post_id}", response_model=Post_Service.schemas.PostOut)
# def get_post(post_id: int, db: Session = Depends(get_db)):
#     post = db.query(Post_Service.models.Post).filter(Post_Service.models.Post.id == post_id).first()
#     if not post:
#         raise HTTPException(status_code=404, detail="Post not found")
#     return post

# @router.post("/posts/", response_model=Post_Service.schemas.PostOut)
# def create_post(post: Post_Service.schemas.PostCreate, username: str = Depends(get_current_user), db: Session = Depends(get_db)):
#     db_post = Post_Service.models.Post(**post.dict(), author_username=username)
#     db.add(db_post)
#     db.commit()
#     db.refresh(db_post)
#     return db_post


# @router.put("/posts/{post_id}", response_model=Post_Service.schemas.PostOut)
# def update_post(post_id: int, post: Post_Service.schemas.PostUpdate, username: str = Depends(verify_token), db: Session = Depends(get_db)):
#     db_post = db.query(Post_Service.models.Post).filter(Post_Service.models.Post.id == post_id).first()
#     if not db_post:
#         raise HTTPException(status_code=404, detail="Post not found")
#     if db_post.author_username != username:
#         raise HTTPException(status_code=403, detail="Not authorized to update this post")
    
#     if post.title:
#         db_post.title = post.title
#     if post.content:
#         db_post.content = post.content
#     db.commit()
#     db.refresh(db_post)
#     return db_post

# @router.delete("/posts/{post_id}")
# def delete_post(post_id: int, username: str = Depends(verify_token), db: Session = Depends(get_db)):
#     db_post = db.query(Post_Service.models.Post).filter(Post_Service.models.Post.id == post_id).first()
#     if not db_post:
#         raise HTTPException(status_code=404, detail="Post not found")
#     if db_post.author_username != username:
#         raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    
#     db.delete(db_post)
#     db.commit()
#     return {"detail": "Post deleted"}














from fastapi import FastAPI, Depends, HTTPException, Header, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List

from Auth.main import get_current_user
from Auth.models import User

import Post_Service.models, Post_Service.schemas

# ---------------- Database ----------------
DATABASE_URL = "postgresql://postgres:nayak@localhost:5432/abc"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Post_Service.models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# ---------------- DB Dependency ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- Post Endpoints ----------------

@router.get("/posts/", response_model=List[Post_Service.schemas.PostOut])
def get_posts(db: Session = Depends(get_db)):
    """Get all posts"""
    return db.query(Post_Service.models.Post).all()


@router.get("/posts/{post_id}", response_model=Post_Service.schemas.PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Get a single post by ID"""
    post = db.query(Post_Service.models.Post).filter(Post_Service.models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("/posts/", response_model=Post_Service.schemas.PostOut)
def create_post(
    post: Post_Service.schemas.PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new post"""
    db_post = Post_Service.models.Post(**post.dict(), author_username=current_user.username)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.put("/posts/{post_id}", response_model=Post_Service.schemas.PostOut)
def update_post(
    post_id: int,
    post: Post_Service.schemas.PostUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a post if the current user is the author"""
    db_post = db.query(Post_Service.models.Post).filter(Post_Service.models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.author_username != current_user.username:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")
    
    if post.title:
        db_post.title = post.title
    if post.content:
        db_post.content = post.content

    db.commit()
    db.refresh(db_post)
    return db_post


@router.delete("/posts/{post_id}")
def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a post if the current user is the author"""
    db_post = db.query(Post_Service.models.Post).filter(Post_Service.models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.author_username != current_user.username:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    
    db.delete(db_post)
    db.commit()
    return {"detail": "Post deleted"}
