from pydantic import BaseModel
from uuid import uuid4
from src.schemas.content import Movie, TvShow
from src.schemas.user import UserModel
from datetime import datetime

class Comment(BaseModel):
    id: str = str(uuid4())
    author: str
    content: str

class Post(BaseModel):
    id: str = str(uuid4())
    author: str
    title: str
    content: str
    num_likes: int = 0
    users_who_liked: list[UserModel]
    num_comments: int = 0
    comments: list[Comment]
    topic: Movie | TvShow
    posted: datetime
