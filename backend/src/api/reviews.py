from fastapi import APIRouter, HTTPException
from src.schemas.reviews import ContentReview
from src.service.impl.content_service import ContentService
from src.db.database import getDB, saveDB

router = APIRouter()

@router.post("", status_code = 201, tags = ["reviews"], response_model = ContentReview)
async def add_review(review: ContentReview):
    db = getDB()

    review_dict = review.model_dump()

    # I have to check if the content exists first
    content = ContentService.get_content_by_id(content_id = review_dict["content_id"], content_type = review_dict["content_type"])

    if content is None: 
        raise HTTPException(status_code = 404, detail = "This content does not exist in the database") 

    # Checking if a review from this user was already made for this content
    for _review in db["reviews"]:
        if review_dict["content_id"] == _review["content_id"] and review_dict["content_type"] == _review["content_type"] and review_dict["username"] == _review["username"]:
            raise HTTPException(status_code = 402, detail = "This user already made a review of this content") 
    
    db["reviews"].append(review_dict)
    saveDB(db)

    return review

@router.get("/{content_type}/{content_id}/rating", status_code = 200, tags = ["reviews"], response_model = float)
async def get_rating_content(content_type: str, content_id: str):
    db = getDB()

    content = ContentService.get_content_by_id(content_id = content_id, content_type = content_type)

    if content is None: 
        raise HTTPException(status_code = 404, detail = "This content does not exist in the database") 

    rating = 0
    count = 0
    for review in db["reviews"]:
        if review["content_type"] == content_type and review["content_id"] == content_id:
            rating += review["rating"]
            count += 1
    if count == 0:
        return 0
    return rating / count

#  Reviews from a user to a content
@router.get("/{username}/{content_type}/{content_id}", status_code = 200, tags = ["reviews"], response_model = ContentReview)
async def get_review_user_content(username: str, content_type: str, content_id: str):
    db = getDB()

    content = ContentService.get_content_by_id(content_id = content_id, content_type = content_type)

    if content is None: 
        raise HTTPException(status_code = 404, detail = "This content does not exist in the database") 

    for review in db["reviews"]:
        if review["username"] == username and review["content_type"] == content_type and review["content_id"] == content_id:
            return review
    raise HTTPException(status_code = 404, detail = "No review from this user to this content found in the database") 

# Reviews to a content
@router.get("/{content_type}/{content_id}", status_code = 200, tags = ["reviews"], response_model = list[ContentReview])
async def get_review_content(content_type: str, content_id: str):
    db = getDB()

    content = ContentService.get_content_by_id(content_id = content_id, content_type = content_type)

    if content is None: 
        raise HTTPException(status_code = 404, detail = "This content does not exist in the database") 


    reviews_to_content = []
    for review in db["reviews"]:
        if review["content_type"] == content_type and review["content_id"] == content_id:
            reviews_to_content.append(review)
    return reviews_to_content

# Reviews from a user
@router.get("/{username}", status_code = 200, tags = ["reviews"], response_model = list[ContentReview])
async def get_review_user(username: str):
    db = getDB()
    reviews_from_user = []
    for review in db["reviews"]:
        if review["username"] == username:
            reviews_from_user.append(review)
    return reviews_from_user

# Get all reviews
@router.get("", status_code = 200, tags = ["reviews"], response_model = list[ContentReview])
async def get_all_reviews():
    db = getDB()
    return db["reviews"]


@router.put("/{username}/{content_type}/{content_id}", status_code = 200, tags = ["reviews"], response_model = ContentReview)
async def update_review(username: str, content_type: str, content_id: str, review: ContentReview):
    db = getDB()

    review_dict = review.model_dump()
    found = False
    
    for i in range(len(db["reviews"])):
        if db["reviews"][i]["username"] == username and db["reviews"][i]["content_type"] == content_type and db["reviews"][i]["content_id"] == content_id:
            found = True
            db["reviews"][i] = review_dict
            break

    if not found:
        raise HTTPException(status_code=404, detail = "No review from this user to this content found in the database")

    saveDB(db)
    return review


@router.delete("/{username}/{content_type}/{content_id}", status_code = 200, tags = ["reviews"], response_model = ContentReview)
async def delete_review(username: str, content_type: str, content_id: str):
    db = getDB()

    found = False
    for i in range(len(db["reviews"])):
        if db["reviews"][i]["username"] == username and db["reviews"][i]["content_type"] == content_type and db["reviews"][i]["content_id"] == content_id:
            found = True
            deleted_review = db["reviews"].pop(i)
            break

    if not found:
        raise HTTPException(status_code=404, detail = "No review from this user to this content in the database")

    saveDB(db)
    return deleted_review
    