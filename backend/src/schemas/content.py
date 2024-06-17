from pydantic import BaseModel
from uuid import uuid4

class Movie(BaseModel):
    id: str = str(uuid4())
    title: str
    synopsis: str
    gender: str
    duration: int 
    release_year: int
    director: str
    main_cast: list[str] 
    banner: str | None = None
    where_to_watch: list[str] = []
    rating: float = 0.0

class TvShow(BaseModel):
    id: str = str(uuid4())
    title: str
    synopsis: str
    gender: str
    num_seasons: int
    num_episodes: int
    release_year: int
    creator: str
    main_cast: list[str]
    banner: str | None = None
    where_to_watch: list[str] = []
    rating: float = 0.0

class Category(BaseModel):
    category_id: str
    items_list: list[TvShow | Movie] = []
