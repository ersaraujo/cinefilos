from src.schemas.content import Movie, TvShow
from src.db.database import getDB, saveDB

class ContentService:
    @staticmethod
    def get_contents(content_type):
        db = getDB()
        
        return db[content_type]

    @staticmethod
    def get_content_by_title(content_title: str, content_type: str):
        db = getDB()
        for content in db[content_type]:
            if content["title"] == content_title:
                return content
        return None

    @staticmethod
    def get_content_by_id(content_id: str, content_type: str):
        db = getDB()
        for content in db[content_type]:
            if content["id"] == content_id:
                return content
        return None

    @staticmethod
    def add_content(content: Movie | TvShow, content_type: str):
        db = getDB()

        content_dict = content.model_dump()
        for _content in db[content_type]:
            if content_dict["title"] == _content["title"]:
                return None
            
        db[content_type].append(content_dict)
        saveDB(db)
        return content
    
    @staticmethod
    def update_content(content_title:str, content: Movie | TvShow, content_type: str):
        db = getDB()

        content_dict = content.model_dump()
        found = False
        for i in range(len(db[content_type])):
            if db[content_type][i]["title"] == content_title:
                found = True
                db[content_type][i] = content_dict
                break

        if not found:
            return None

        saveDB(db)
        return content
    
    @staticmethod
    def delete_content(content_title: str, content_type: str):
        db = getDB()

        found = False
        for i in range(len(db[content_type])):
            if db[content_type][i]["title"] == content_title:
                found = True
                deleted_content = db[content_type].pop(i)
                break

        if not found:
            return None

        saveDB(db)
        return deleted_content