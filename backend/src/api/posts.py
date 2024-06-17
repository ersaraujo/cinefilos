from fastapi import APIRouter, HTTPException
from src.db.database import getDB, saveDB
from src.schemas.forum import Post, Comment
from src.schemas.user import UserModel
from src.service.impl.post_service import PostService
import typing as ty

router = APIRouter()

@router.post("/newpost", status_code=201, tags=["forum"], response_model=Post)
async def create_post(post: Post):
    db = getDB()

    post_dict = post.model_dump()
    if post["title"] == None:
        raise HTTPException(status_code=422, detail="Não é possível publicar um post sem título")
    elif post["content"] == None:
        raise HTTPException(status_code=422, detail="Não é possível publicar um post sem conteúdo")
        
    db["posts"].append(post_dict)
    saveDB(db)
    return post

@router.delete("/post/{post_id}", status_code=200, tags=["forum"], response_model=Post)
async def remove_post(post_id: str):
    db = getDB()

    found = False
    for i in range(len(db["posts"])):
        if db["posts"][i]["id"] == post_id:
            found = True
            deleted_post = db["posts"].pop(i)
            break

    if not found:
        raise HTTPException(status_code=404, detail="Este post não existe ou já foi excluído")

    saveDB(db)
    return deleted_post

@router.get("/feed", status_code=200, tags=["forum"], response_model=list[Post])
async def get_posts():
    db = getDB()
    return db["posts"]

@router.get("/post/{post_id}", status_code=200, tags=["forum"], response_model=Post)
async def open_post(post_id: str):
    post = PostService.get_post_by_id(post_id)
    
    if post is None:
        raise HTTPException(status_code=404, detail="Este post não existe ou foi excluído")
    
    return post

@router.put("/post/{post_id}", status_code=200, tags=["forum"], response_model=ty.Tuple[UserModel, bool])
async def update_like(post_id: str, user_id: str):
    db = getDB()

    found = False
    for post_ in db["posts"]:
        if post_["id"] == post_id:
            found = True
            post = post_
    
    if not found:
        raise HTTPException(status_code=404, detail="Este post não existe ou foi excluído")

    already_liked = False
    for i in range(len(post["users_who_liked"])):
        if post["users_who_liked"][i]["id"] == user_id:
            already_liked = True
            user = post["users_who_liked"].pop(i)
            post["num_likes"] -= 1
            saveDB(db)
            return (user, False)

    if not already_liked:
        post["users_who_liked"].append(user)
        post["num_likes"] += 1
        saveDB(db)
        return (user, True)

@router.get("/post/{post_id}/likes", status_code=200, tags=["forum"], response_model=list[UserModel])
async def get_likes_list(post_id: str):
    db = getDB()
    
    found = False
    for post in db["posts"]:
        if post["id"] == post_id:
            found = True
            return post["users_who_liked"]

    if not found:
        raise HTTPException(status_code=404, detail="Este post não existe ou foi excluído")

@router.get("/search/{topic}", status_code = 200, tags = ["forum"], response_model=list[Post])
async def get_posts_from_topic(topic: str):
    db = getDB()

    posts_from_topic = []
    for post in db["posts"]:
        if post["topic"] == topic:
            posts_from_topic.append(post)
    return posts_from_topic

@router.post("/post/{post_id}", status_code = 200, tags = ["forum"], response_model=Comment)
async def add_comment(post_id: str, comment: Comment):
    db = getDB()

    for i in range(len(db["posts"])):
        if db["posts"][i]["id"] == post_id:
            db["posts"][i]["comments"].append(comment)
            db["posts"][i]["num_comments"] += 1
            saveDB(db)
            return comment

    raise HTTPException(status_code = 404, detail = "Este post não existe ou foi excluído")

@router.delete("/post/{post_id}", status_code = 200, tags = ["forum"], response_model=Comment)
async def remove_comment(post_id: str, comment_id: str):
    db = getDB()

    found_post = False
    for i in range(len(db["posts"])):
        if db["posts"][i]["id"] == post_id:
            found_post = True
            for j in range(len(db["posts"][i]["comments"])):
                if db["posts"][i]["comments"][j]["id"] == comment_id:
                    db["posts"][i]["comments"].pop(j)
                    db["posts"][i]["num_comments"] -= 1
                    saveDB(db)
                    return db["posts"][i]["comments"][j]

    if not found_post:
        raise HTTPException(status_code = 404, detail = "Este post não existe ou foi excluído")
    else:
        raise HTTPException(status_code = 404, detail = "Este comentário não existe ou já foi excluído")
