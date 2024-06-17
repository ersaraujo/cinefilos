from pytest import raises
from fastapi import HTTPException
from src.db.database import getDB, saveDB, clearDB
from pytest_bdd import parsers, given, when, then, scenario
from src.service.impl.watch_list_service import WatchListService
from src.service.impl.content_service import ContentService
from src.schemas.content import Movie, TvShow, Category

@scenario(scenario_name="Add movie to category", feature_name="../features/watch_list.feature")
def test_add_to_category():
    """ Scenario Scope """

@given(parsers.cfparse('no movie with title "{title}" is in the "{category}" list of the user "{username}"'))
def check_movie_title_not_found(client, title: str, category: str, username: str):
    db = getDB()
    db["user"][username][category] = []
    saveDB(db)

@given(parsers.cfparse('movie with title "{title}", content_id "{content_id}" is in the database'))
def mock_movie_in_db(title: str, content_id: str):
    ContentService.add_content(Movie(
        id=content_id,
        title=title, 
        synopsis="random synopsis",
        gender="random gender",
        duration=0,
        release_year=0,
        director="random director",
        main_cast=[]
    ), "movies")

@when(
    parsers.cfparse('a POST request is sent to the list "{category}" of the user "{username}", content_id "{content_id}"'),
    target_fixture="context"
)
def post_movie_to_category(client, context, category: str, username: str, content_id: str):
    response = client.post(
        '/watch_list/user',
        params={
            "username": username,
            "category": category,
            "content_id": content_id,
            "content_type": "movies"
        }
    )

    context["response"] = response
    return context

@then(parsers.cfparse('the json status code is "{status_code}"'), target_fixture="context")
def check_response_status_code(context, status_code: str):
    assert context["response"].status_code == int(status_code)

    return context

@then(
    parsers.cfparse('the json response have title "{title}", content_id "{content_id}"'),
    target_fixture="context"
)
def check_response_body(context, title: str, content_id: str):
    response_body = context["response"].json()

    assert response_body["title"] == title
    assert response_body["id"] == content_id

    return context

@scenario(scenario_name="Add movie that is already in category", feature_name="../features/watch_list.feature")
def test_add_already_in_category():
    """ Scenario Scope """

@given(parsers.cfparse('movie with title "{title}" is in the "{category}" list of the user "{username}"'))
def check_movie_title_found(client, title: str, category: str, username: str):
    post_response = client.post(
        f'/watch_list/{title}',
        params={
            "username": username,
            "category": category,
            "title": title,
            "content_type": "movies"
        }
    )

@then(parsers.cfparse('the json response have message "{response_message}"'))
def check_response_message(context, response_message: str):
    assert context["response"].json()["detail"] == response_message
    return context

@scenario(scenario_name="Add movie that is not in database to category", feature_name="../features/watch_list.feature")
def test_add_not_in_db():
    """ Scenario Scope """

@given(parsers.cfparse('no movie with title "{title}" is in the database'))
def check_movie_not_in_db(client, title: str):
    db = getDB()
    clearDB(db)

@scenario(scenario_name="Get movie from category list", feature_name="../features/watch_list.feature")
def test_get_movie_from_category():
    """ Scenario Scope """

@when(
    parsers.cfparse('a GET request is sent to the list "{category}" of the user "{username}"'),
    target_fixture="context"
)
def post_movie_to_category(client, context, category: str, username: str):
    response = client.get(
        f'/watch_list/user/{username}/{category}'
    )

    context["response"] = response
    return context

@then(parsers.cfparse('the json response contains the movie with title "{title}"'), target_fixture="context")
def check_movie_in_response(context, title: str):
    response_body = context["response"].json()
    assert any(m["title"] == title for m in response_body["items_list"])
    return context

@scenario(scenario_name="Get category list", feature_name="../features/watch_list.feature")
def test_get_category_list():
    """ Scenario Scope """

@given(parsers.cfparse('user with username "{username}" is in the database'))
def check_user_in_db(username: str):
    db = getDB()
    if username not in db["user"]:
        db["user"][username] = {"assistidos": [], "assistindo": [], "quero_assistir": []}

@then(parsers.cfparse('the json response contains a items_list'), target_fixture="context")
def check_item_list(context):
    response_body = context["response"].json()

    assert "items_list" in response_body
    return context
    
@scenario(scenario_name="Remove movie from category", feature_name="../features/watch_list.feature")
def test_remove_from_category():
    """ Scenario Scope """

@when(
    parsers.cfparse('a DELETE request is sent to the list "{category}" of the user "{username}", content_id "{content_id}"'),
    target_fixture="context"
)
def delete_from_category(client, context, category: str, username: str, content_id: str):
    response = client.delete(
        f'/watch_list/user/{username}/{category}',
        params={
            "username": username,
            "category": category,
            "content_id": content_id,
            "content_type": "movies"
        }
    )

    # with raises(HTTPException) as exc_info:
    context["response"] = response
    return context

@scenario(scenario_name="Remove movie not in the category", feature_name="../features/watch_list.feature")
def test_remmove_not_in_category():
    """ Scenario scope """
