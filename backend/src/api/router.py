from fastapi import APIRouter
from src.api import items
from src.api import contents
from src.api import posts
from src.api import reviews
from src.api import watch_list

api_router = APIRouter()
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(contents.router, prefix="/contents", tags=["contents"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
api_router.include_router(watch_list.router, prefix="/watch_list", tags=["watch_list"])
api_router.include_router(posts.router, prefix="/forum", tags=["forum"])
