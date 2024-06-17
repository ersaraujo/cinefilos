from src.schemas.reviews import ContentReview
from src.db.database import getDB, saveDB

class ReviewService:
    @staticmethod 
    def get_reviews():
        db = getDB()
        return db["reviews"]


    @staticmethod 
    def get_reviews_from_user(username: str):
        db = getDB()
        reviews_from_user = []
        for review in db["reviews"]:
            if review["username"] == username:
                reviews_from_user.append(review)
        return reviews_from_user
    
    @staticmethod 
    def get_reviews_from_content(content_type: str, content_id: str):
        db = getDB()
        reviews_from_content = []
        for review in db["reviews"]:
            if review["content_type"] == content_type and review["content_id"] == content_id:
                reviews_from_content.append(review)
        return reviews_from_content
    
    @staticmethod
    def get_rating_from_content(content_type: str, content_id: str):
        db = getDB()
        rating = 0
        count = 0
        for review in db["reviews"]:
            if review["content_type"] == content_type and review["content_id"] == content_id:
                rating += review["rating"]
                count += 1
        if count == 0:
            return 0
        return rating / count

    @staticmethod
    def add_review(review: ContentReview):
        db = getDB()

        review_dict = review.model_dump()
        for _review in db["reviews"]:
            if review_dict["content_id"] == _review["content_id"] and review_dict["content_type"] == _review["content_type"] and review_dict["username"] == _review["username"]:
                return None
            
        db["reviews"].append(review_dict)
        saveDB(db)
        return review
    
    @staticmethod
    def update_review(review: ContentReview):
        db = getDB()

        review_dict = review.model_dump()
        found = False

        for i in range(len(db["reviews"])):
            if db["reviews"][i]["username"] == review_dict["username"] and db["reviews"][i]["content_type"] == review_dict["content_type"] and db["reviews"][i]["content_id"] == review_dict["content_id"]:
                found = True
                db["reviews"][i] = review_dict

        if not found:
            return None

        saveDB(db)
        return review
    
    @staticmethod
    def delete_review(username: str, content_type: str, content_id: str):
        db = getDB()

        found = False
        for i in range(len(db["reviews"])):
            if db["reviews"][i]["username"] == username and db["reviews"][i]["content_type"] == content_type and db["reviews"][i]["content_id"] == content_id:
                found = True
                deleted_review = db["reviews"].pop(i)
                break

        if not found:
            return None

        saveDB(db)
        return deleted_review