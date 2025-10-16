# from pydantic import BaseModel
# from datetime import datetime

# class CommentCreate(BaseModel):
#     content: str

# class CommentOut(BaseModel):
#     id: int
#     post_id: int
#     author_username: str
#     content: str
#     created_at: datetime

#     class Config:
#          orm_mode = True


from pydantic import BaseModel
from datetime import datetime

class CommentCreate(BaseModel):
    content: str


class CommentOut(BaseModel):
    id: int
    post_id: int
    author_username: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True   # ✅ replaces orm_mode in Pydantic v2
