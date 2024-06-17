from fastapi import APIRouter, HTTPException
from src.schemas.content import Movie, TvShow, Category
from src.db.database import getDB, saveDB

class WatchListService:
    @staticmethod
    def add_to_category_list(username: str, category_id: str, content_id: str, content_type: str):
        db = getDB()

        for content in db[content_type]:
            if content["id"] == content_id:
                if content not in db["user"][username][category_id]:
                    db["user"][username][category_id].append(content)
                    saveDB(db)
                else:
                    raise HTTPException(status_code=422, detail="This movie is already in the category")
                return content
        
        raise HTTPException(status_code=404, detail="No movie with this ID found in the database")
    
    @staticmethod
    def add_to_category_list_by_title(username: str, category_id: str, title: str, content_type: str):
        db = getDB()

        for content in db[content_type]:
            if content["title"] == title:
                if content not in db["user"][username][category_id]:
                    db["user"][username][category_id].append(content)
                    saveDB(db)
                else:
                    raise HTTPException(status_code=422, detail="This movie is already in the category")
                return content
        
        raise HTTPException(status_code=404, detail="No movie with this ID found in the database")

    @staticmethod
    def get_category_list(username: str, category_id: str):
        db = getDB()

        return db["user"][username][category_id]
    
    @staticmethod
    def delete_of_category_list(username: str, category_id: str, content_id: str, content_type: str):
        db = getDB()

        for i in range(len(db["user"][username][category_id])):
            if db["user"][username][category_id][i]["id"] == content_id:
                deleted_content = db["user"][username][category_id].pop(i)
                saveDB(db)
                return deleted_content
                break

        raise HTTPException(status_code=404, detail="No movie with this ID found in this category")

    @staticmethod
    def delete_of_category_list_by_title(username: str, category_id: str, title: str, content_type: str):
        db = getDB()

        for i in range(len(db["user"][username][category_id])):
            if db["user"][username][category_id][i]["title"] == title:
                deleted_content = db["user"][username][category_id].pop(i)
                saveDB(db)
                return deleted_content
                break

        raise HTTPException(status_code=404, detail="No movie with this ID found in this category")
