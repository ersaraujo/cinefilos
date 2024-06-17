from fastapi import APIRouter, HTTPException
from src.schemas.content import Movie, TvShow
from src.service.impl.content_service import ContentService

router = APIRouter()

@router.post("/movies", status_code=201, tags=["movie"], response_model=Movie)
async def add_movie(movie: Movie):
    added_movie = ContentService.add_content(movie, "movies")
    
    if added_movie is None:
        raise HTTPException(status_code=422, detail="There is a movie with the same title in the database")
    
    return added_movie

@router.post("/tv_shows", status_code=201, tags=["tv show"], response_model=TvShow)
async def add_tv_show(tv_show: TvShow):
    added_tv_show = ContentService.add_content(tv_show, "tv_shows")
    
    if added_tv_show is None:
        raise HTTPException(status_code=422, detail="There is a tv show with the same title in the database")
    
    return added_tv_show

@router.get("/movies/{movie_title}", status_code=200, tags=["movie"], response_model=Movie)
async def get_movie_by_title(movie_title: str):
    movie = ContentService.get_content_by_title(movie_title, "movies")
    
    if movie is None:
        raise HTTPException(status_code=404, detail="No movie with this title found in the database")
    
    return movie

@router.get("/tv_shows/{tv_show_title}", status_code=200, tags=["tv show"], response_model=TvShow)
async def get_tv_show_by_title(tv_show_title: str):
    tv_show = ContentService.get_content_by_title(tv_show_title, "tv_shows")
    
    if tv_show is None:
        raise HTTPException(status_code=404, detail="No tv show with this title found in the database")

    return tv_show

@router.get("/movies", status_code=200, tags=["movie"], response_model=list[Movie])
async def get_movies():
    movies = ContentService.get_contents("movies")
    
    return movies

@router.get("/tv_shows", status_code=200, tags=["tv show"], response_model=list[TvShow])
async def get_tv_shows():
    tv_shows = ContentService.get_contents("tv_shows")

    return tv_shows

@router.get("/", status_code=200, response_model=list[Movie | TvShow])
async def get_contents():
    movies = ContentService.get_contents("movies")
    tv_shows = ContentService.get_contents("tv_shows")

    return movies + tv_shows

@router.put("/movies/{movie_title}", status_code=200, tags=["movie"], response_model=Movie)
async def update_movie(movie_title: str, movie: Movie):
    updated_movie = ContentService.update_content(movie_title, movie, "movies") 

    if updated_movie is None:
        raise HTTPException(status_code=404, detail="No movie with this title found in the database")

    return updated_movie

@router.put("/tv_shows/{tv_show_title}", status_code=200, tags=["tv show"], response_model=TvShow)
async def update_tv_show(tv_show_title: str, tv_show: TvShow):
    updated_tv_show = ContentService.update_content(tv_show_title, tv_show, "tv_shows") 

    if updated_tv_show is None:
        raise HTTPException(status_code=404, detail="No tv show with this title found in the database")

    return updated_tv_show

@router.delete("/movies/{movie_title}", status_code=200, tags=["movie"], response_model=Movie)
async def delete_movie(movie_title: str):
    deleted_movie = ContentService.delete_content(movie_title, "movies")

    if deleted_movie is None:
        raise HTTPException(status_code=404, detail="No movie with this title found in the database")

    return deleted_movie

@router.delete("/tv_shows/{tv_show_title}", status_code=200, tags=["tv show"], response_model=TvShow)
async def delete_tv_show(tv_show_title: str):
    deleted_tv_show = ContentService.delete_content(tv_show_title, "tv_shows")

    if deleted_tv_show is None:
        raise HTTPException(status_code=404, detail="No tv show with this title found in the database")

    return deleted_tv_show