from pydantic import BaseModel

class ContentReview(BaseModel):
    title: str = ""
    report: str
    rating: float = 0.0
    username: str
    content_id: str
    content_type: str

    