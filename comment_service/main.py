
# from fastapi import FastAPI, Depends, HTTPException, Header,APIRouter
# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from jose import jwt, JWTError
# from typing import List
# from pydantic import BaseModel

# import comment_service.models, comment_service.schemas

# # ---------------- Database ----------------
# DATABASE_URL = "postgresql://postgres:nayak@localhost:5432/abc"
# SECRET = "secret"
# ALGORITHM = "HS256"

# # Remove `check_same_thread` for PostgreSQL
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# comment_service.models.Base.metadata.create_all(bind=engine)

# router = APIRouter()

# # ---------------- DB Dependency ----------------
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # ---------------- JWT Verification ----------------
# def verify_token(authorization: str = Header(...)):
#     if not authorization.startswith("Bearer "):
#         raise HTTPException(status_code=401, detail="Invalid authorization header")
#     token = authorization.split(" ")[1]
#     try:
#         payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
#         return payload.get("username")
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")

# # ---------------- Auth comment_service.Models ----------------
# class AuthRequest(BaseModel):
#     username: str

# class AuthResponse(BaseModel):
#     access_token: str

# # ---------------- Auth Endpoint ----------------
# @router.post("/authorize", response_model=AuthResponse)
# def authorize(auth: AuthRequest):
#     if not auth.username:
#         raise HTTPException(status_code=400, detail="Username required")
#     token = jwt.encode({"username": auth.username}, SECRET, algorithm=ALGORITHM)
#     return {"access_token": token}

# # ---------------- Comment Endpoints ----------------
# @router.get("/posts/{post_id}/comments", response_model=List[comment_service.schemas.CommentOut])
# def get_comments(post_id: int, db: Session = Depends(get_db)):
#     return db.query(comment_service.models.Comment).filter(comment_service.models.Comment.post_id == post_id).all()

# @router.post("/posts/{post_id}/comments", response_model=comment_service.schemas.CommentOut)
# def create_comment(
#     post_id: int,
#     comment: comment_service.schemas.CommentCreate,
#     username: str = Depends(verify_token),
#     db: Session = Depends(get_db)
# ):
#     db_comment = comment_service.models.Comment(
#         post_id=post_id,
#         content=comment.content,
#         author_username=username
#     )
#     db.add(db_comment)
#     db.commit()
#     db.refresh(db_comment)
#     return db_comment

# @router.delete("/comments/{comment_id}")
# def delete_comment(
#     comment_id: int,
#     username: str = Depends(verify_token),
#     db: Session = Depends(get_db)
# ):
#     db_comment = db.query(comment_service.models.Comment).filter(comment_service.models.Comment.id == comment_id).first()
#     if not db_comment:
#         raise HTTPException(status_code=404, detail="Comment not found")
#     if db_comment.author_username != username:
#         raise HTTPException(status_code=403, detail="Not authorized to delete this comment")

#     db.delete(db_comment)
#     db.commit()
#     return {"detail": "Comment deleted"}




from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List

from Auth.main import get_current_user   # ✅ reuse same JWT auth
from Auth.models import User

import comment_service.models, comment_service.schemas

# ---------------- Database ----------------
DATABASE_URL = "postgresql://postgres:nayak@localhost:5432/abc"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
comment_service.models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# ---------------- DB Dependency ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- Comment Endpoints ----------------

@router.get("/posts/{post_id}/comments", response_model=List[comment_service.schemas.CommentOut])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    """Fetch all comments for a post"""
    return (
        db.query(comment_service.models.Comment)
        .filter(comment_service.models.Comment.post_id == post_id)
        .all()
    )


@router.post("/posts/{post_id}/comments", response_model=comment_service.schemas.CommentOut)
def create_comment(
    post_id: int,
    comment: comment_service.schemas.CommentCreate,
    current_user: User = Depends(get_current_user),   # ✅ user comes from Auth service
    db: Session = Depends(get_db),
):
    """Create a comment (must be logged in)"""
    db_comment = comment_service.models.Comment(
        post_id=post_id,
        content=comment.content,
        author_username=current_user.username,
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


@router.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_user),   # ✅ secure delete
    db: Session = Depends(get_db),
):
    """Delete a comment (only by its author)"""
    db_comment = (
        db.query(comment_service.models.Comment)
        .filter(comment_service.models.Comment.id == comment_id)
        .first()
    )
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.author_username != current_user.username:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")

    db.delete(db_comment)
    db.commit()
    return {"detail": "Comment deleted"}


# ---------------- App Init ----------------
app = FastAPI(title="Comment Service API")
app.include_router(router, prefix="/comments", tags=["Comments"])
