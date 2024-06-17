from fastapi import APIRouter
from src.schemas.content import Movie, TvShow, Category
from src.db.database import getDB, saveDB
from src.service.impl.watch_list_service import WatchListService

router = APIRouter()

@router.post("/user/", status_code = 201, tags = ["watch_list"], response_model = Movie | TvShow)
async def add_to_category_list(username: str, category: str, content_id: str, content_type: str):
    added_content = WatchListService.add_to_category_list(username, category, content_id, content_type)

    return added_content

@router.post("/{title}/", status_code = 201, tags = ["watch_list"], response_model = Movie | TvShow)
async def add_to_category_list(username: str, category: str, title: str, content_type: str):
    added_content = WatchListService.add_to_category_list_by_title(username, category, title, content_type)

    return added_content

@router.get("/user/{username}/{category}", status_code = 200, tags = ["watch_list"], response_model = Category)
async def get_category_list(username: str, category: str):
    category_list = WatchListService.get_category_list(username, category)
    category_result = Category(category_id=category, items_list=category_list)

    return category_result

@router.delete("/user/{username}/{category}", status_code = 200, tags = ["watch_list"], response_model = Movie | TvShow)
async def get_category_list(username: str, category: str, content_id: str, content_type: str):
    removed_content = WatchListService.delete_of_category_list(username, category, content_id, content_type)

    return removed_content

@router.delete("/user/{username}/{category}/{title}", status_code = 200, tags = ["watch_list"], response_model = Movie | TvShow)
async def get_category_list(username: str, category: str, title: str, content_type: str):
    removed_content = WatchListService.delete_of_category_list_by_title(username, category, title, content_type)

    return removed_content

