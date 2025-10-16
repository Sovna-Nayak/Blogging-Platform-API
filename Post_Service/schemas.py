# from pydantic import BaseModel
# from datetime import datetime
# from typing import Optional

# # ---------- Base ----------
# class PostBase(BaseModel):
#     title: str
#     content: str

# # ---------- Create ----------
# class PostCreate(PostBase):
#     pass

# # ---------- Update ----------
# class PostUpdate(BaseModel):
#     title: Optional[str] = None
#     content: Optional[str] = None

# # ---------- Output ----------
# class PostOut(PostBase):
#     id: int
#     author_username: str
#     created_at: datetime
#     updated_at: Optional[datetime]

#     class Config:
#         orm_mode = True


from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# ---------------- Post Service Schemas ----------------

class PostCreate(BaseModel):
    title: str
    content: str

class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    author_username: str
    created_at: datetime
    updated_at: Optional[datetime] = None  # <-- make it optional

    class Config:
        orm_mode = True

# ---------------- Comment Service Schemas ----------------

class CommentCreate(BaseModel):
    content: str

class CommentOut(BaseModel):
    id: int
    post_id: int
    author_username: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
