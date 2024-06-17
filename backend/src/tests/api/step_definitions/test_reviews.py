from src.db.database import getDB, clearDB, clearDBReviews, clearDBContent
from pytest_bdd import parsers, given, when, then, scenario
from src.service.impl.review_service import ReviewService
from src.schemas.reviews import ContentReview
from src.schemas.content import Movie, TvShow
from src.service.impl.content_service import ContentService

@scenario(scenario_name="Register a movie review on the database", feature_name="../features/reviews.feature")  
def test_register_review_movies():
    db = getDB()
    clearDB(db)

@given(parsers.cfparse('no review from username "{username}" to content_id "{content_id}", content_type "{content_type}" is in database'))  
def mock_review_service_clean(username: str, content_id: str, content_type: str):
    db = getDB()
    clearDB(db)

@given(parsers.cfparse('content with content_id "{content_id}" and content_type "{content_type}" exists in the database'))
def mock_add_content(content_id: str, content_type: str):
    db = getDB()
    clearDBContent(db)

    if content_type == "movies":
        add_content = ContentService.add_content(Movie(title="interstellar", synopsis="Sinopse", gender = "ficcao cientifica", duration = 120, release_year = 2022, 
                                                   director = "Christopher Nolan", main_cast = ["Matthew McConaughey", "Anne Hathaway"], banner = "banner.png", id = content_id), content_type)
    else:
        add_content = ContentService.add_content(TvShow(title="Breaking Bad", synopsis = "Sinopse", gender = "drama", num_seasons = 5, num_episodes = 62, release_year = 2008, 
                                                        creator = "Vince Gilligan", main_cast = ["Bryan Cranston", "Aaron Paul"], banner = "banner.png", id = content_id), content_type)
                                                 
    assert add_content is not None

@when(
    parsers.cfparse('a POST request is sent to "{req_url}" from username "{username}", content_id "{content_id}", content_type "{content_type}", rating "{rating}", report "{report}"'), 
    target_fixture="context"
)
def send_post_review_request(client, context, req_url: str, username: str, content_id: str, content_type: str, rating: float, report: str):

    response = client.post(
        req_url,
        json={
            "username": username,
            "content_id": content_id,
            "content_type": content_type,
            "rating": rating,
            "report": report
        })
    
    context["response"] = response
    return context

@then(
    parsers.cfparse('the json status code is "{status_code}"'), 
    target_fixture="context"
)
def check_json_status_code(context, status_code: str):
    assert context["response"].status_code == int(status_code)
    return context

@then(
    parsers.cfparse('the json response have username "{username}", content_id "{content_id}", content_type "{content_type}", rating "{rating}", report "{report}"'), 
    target_fixture="context"
)
def check_response_json(context, username: str, content_id: str, content_type: str, rating: float, report: str):
    
    json_response = context["response"].json()
    print(json_response)
    assert json_response["username"] == username
    assert json_response["content_id"] == content_id
    assert json_response["content_type"] == content_type
    assert json_response["rating"] == float(rating)
    assert json_response["report"] == report

    return context

@scenario(scenario_name="Register a tv show review on the database", feature_name="../features/reviews.feature")  
def test_register_review_tv_shows():
    db = getDB()
    clearDB(db)

@scenario(scenario_name = "Try to register a movie review to a movie that already has been reviewed by the user", feature_name = "../features/reviews.feature")
def test_register_review_movies_already_reviewed():
    db = getDB()
    clearDB(db)

@given(parsers.cfparse('only a review from username "{username}" to content_id "{content_id}", content_type "{content_type}", rating "{rating}", report "{report}" is in database'))
def mock_review_service(username: str, content_id: str, content_type: str, rating: float, report: str):
    db = getDB()
    clearDBReviews(db)

    add_review = ReviewService.add_review(ContentReview(username=username, content_id=content_id, content_type=content_type, rating=rating, report=report))

    assert add_review is not None

@then(parsers.cfparse('the database have review with username "{username}", content_id "{content_id}", content_type "{content_type}", rating "{rating}", report "{report}"'))
def check_review_service(username: str, content_id: str, content_type: str, rating: float, report: str):
    reviews = ReviewService.get_reviews_from_user(username)

    found = False

    for review in reviews:
        if review["username"] == username and review["content_id"] == content_id and review["content_type"] == content_type:
            assert review["rating"] == float(rating)
            assert review["report"] == report
            found = True
    
    assert found

@scenario(scenario_name="Try to register a tv show review to a tv show that already has been reviewed by the user", feature_name="../features/reviews.feature")
def test_register_review_tv_shows_already_reviewed():
    db = getDB()
    clearDB(db)

@scenario(scenario_name = "Try to register a movie review to a movie that does not exist in the database", feature_name="../features/reviews.feature")
def test_register_review_movies_not_exist():
    db = getDB()
    clearDB(db)

@given(parsers.cfparse('no content with content_id "{content_id}" and content_type "{content_type}" exist in database'))
def mock_content_service_clean(content_id: str, content_type: str):
    db = getDB()
    clearDB(db)

@then(parsers.cfparse('the database does not contain any reviews'))
def check_review_service_empty():
    reviews = ReviewService.get_reviews()
    assert len(reviews) == 0

@scenario(scenario_name="Try to register a tv show review to a tv show that does not exist in the database", feature_name="../features/reviews.feature")
def test_register_review_tv_shows_not_exist():
    db = getDB()
    clearDB(db)

@scenario(scenario_name="Get a review from a user to a content", feature_name="../features/reviews.feature")
def test_get_review_from_user_to_content():
    db = getDB()
    clearDB(db)

@when(
    parsers.cfparse('a GET request is sent to "{req_url}"'), 
    target_fixture="context"
)
def send_get_review_request(client, context, req_url: str):

    response = client.get(req_url)
    
    context["response"] = response
    return context

@scenario(scenario_name="Get review from a user to some content", feature_name="../features/reviews.feature")
def test_get_reviews_from_user():
    db = getDB()
    clearDB(db)

@given(parsers.cfparse('username "{username}" only made "{amount_of_reviews}" reviews'))
def mock_review_service(username: str, amount_of_reviews: int):
    reviews = ReviewService.get_reviews_from_user(username)
    assert len(reviews) == int(amount_of_reviews)
 
@then(parsers.cfparse('the json response have a list of length "{amount_of_reviews}"'))
def check_amount_of_reviews(context, amount_of_reviews: int):
    json_response = context["response"].json()

    assert isinstance(json_response, list)
    assert len(json_response) == int(amount_of_reviews)
    return context

@then(parsers.cfparse('the list in position "{pos}" have username "{username}", content_id "{content_id}", content_type "{content_type}", rating "{rating}", report "{report}"'))
def check_review_list(context, pos: int, username: str, content_id: str, content_type: str, rating: float, report: str):
    json_response = context["response"].json()

    review = json_response[int(pos)]

    assert review["username"] == username
    assert review["content_id"] == content_id
    assert review["content_type"] == content_type
    assert review["rating"] == float(rating)
    assert review["report"] == report

    return context

@scenario(scenario_name="Get all reviews to some content", feature_name="../features/reviews.feature")
def test_get_reviews_to_content():
    db = getDB()
    clearDB(db)

@scenario(scenario_name="Get all reviews in database", feature_name="../features/reviews.feature")
def test_get_all_reviews():
    db = getDB()
    clearDB(db)

@scenario(scenario_name="Get reviews of a content that does not exist in the database", feature_name="../features/reviews.feature")
def test_get_reviews_content_not_exist():
    db = getDB()
    clearDB(db)

@given(parsers.cfparse('no content with content_id "{content_id}" and content_type "{content_type}" exists in the database'))
def mock_content_service_clean(content_id: str, content_type: str):
    db = getDB()
    clearDB(db)

@then(parsers.cfparse('the database does not have content with content_id "{content_id}" and content_type "{content_type}"'))
def check_content_does_not_exist(content_id: str, content_type: str):
    content = ContentService.get_content_by_id(content_id, content_type)
    assert content is None

@scenario(scenario_name="Get reviews from a user to a content that does not exist in the database", feature_name="../features/reviews.feature")
def test_get_reviews_user_content_not_exist():
    db = getDB()
    clearDB(db)

@scenario(scenario_name="Get a review from a user to a content that was not reviewed by the user", feature_name="../features/reviews.feature")
def test_get_review_user_content_not_reviewed():
    db = getDB()
    clearDB(db)

@then(parsers.cfparse('the database does not have review from user "{username}" to content with content_id "{content_id}" and content_type "{content_type}"'))
def check_review_does_not_exist(username: str, content_id: str, content_type: str):
    reviews = ReviewService.get_reviews_from_user(username)

    found = False

    for review in reviews:
        if review["username"] == username and review["content_id"] == content_id and review["content_type"] == content_type:
            found = True
    
    assert not found

@scenario(scenario_name="Update a review from a user to a content in the database", feature_name="../features/reviews.feature")
def test_update_review():
    db = getDB()
    clearDB(db)

@when(
    parsers.cfparse('a PUT request is sent to "{req_url}" from username "{username}", content_id "{content_id}", content_type "{content_type}", rating "{rating}", report "{report}"'), 
    target_fixture="context"
)
def send_put_review_request(client, context, req_url: str, username: str, content_id: str, content_type: str, rating: float, report: str):

    response = client.put(
        req_url,
        json={
            "username": username,
            "content_id": content_id,
            "content_type": content_type,
            "rating": rating,
            "report": report
        })
    
    context["response"] = response
    return context

@scenario(scenario_name="Try to update a review that does not exist", feature_name="../features/reviews.feature")
def test_update_review_not_exist():
    db = getDB()
    clearDB(db)

@scenario(scenario_name="Delete a review from a user to a content", feature_name="../features/reviews.feature")
def test_delete_review():
    db = getDB()
    clearDB(db)

@when(
    parsers.cfparse('a DELETE request is sent to "{req_url}"'), 
    target_fixture="context"
)
def send_delete_review_request(client, context, req_url: str):
    response = client.delete(req_url)
    
    context["response"] = response
    return context

@scenario(scenario_name="Try to delete a review that does not exist in the database", feature_name="../features/reviews.feature")   
def test_delete_review_not_exist():
    db = getDB()
    clearDB(db)

@scenario(scenario_name="Get rating from a content", feature_name="../features/reviews.feature") 
def test_get_rating():
    db = getDB()
    clearDB(db)

@given(parsers.cfparse('a review from username "{username}" to content_id "{content_id}", content_type "{content_type}", rating "{rating}", report "{report}" is in database'))
def mock_review_service(username: str, content_id: str, content_type: str, rating: float, report: str):
    db = getDB()

    add_review = ReviewService.add_review(ContentReview(username=username, content_id=content_id, content_type=content_type, rating=rating, report=report))

    assert add_review is not None

@then(parsers.cfparse('the json response is a float "{rating}"'))
def check_rating(context, rating: float):
    json_response = context["response"].json()

    assert isinstance(json_response, float)
    assert json_response == float(rating)

    return context

@scenario(scenario_name="Get rating from a content that does not exist", feature_name="../features/reviews.feature")
def test_get_rating_not_exist():
    db = getDB()
    clearDB(db)