from src.db.database import getDB, clearDB
from pytest_bdd import parsers, given, when, then, scenario
from src.service.impl.content_service import ContentService
from src.schemas.content import Movie


@scenario(scenario_name="Register a movie on the database", feature_name="../features/movies.feature")
def test_register_movie():
    db = getDB()
    clearDB(db)

@given(parsers.cfparse('no movie with title "{title}" is in the database'))
def mock_movie_service_clean(title: str):
    db = getDB()
    clearDB(db)

@when(
    parsers.cfparse('a POST request is sent to "{req_url}" with title "{title}", synopsis "{synopsis}"'), 
    target_fixture="context"
)
def send_post_movie_request(client, context, req_url: str, title: str, synopsis: str):

    response = client.post(
        req_url,
        json={
            "title": title,
            "synopsis": synopsis,
            "gender": "ação",
            "duration": 120,
            "release_year": 2022,
            "director": "Tarantino",
            "main_cast": ["The Rock", "Xuxa"],
            "banner": "banner.png"
        })
    
    context["response"] = response
    return context

@then(parsers.cfparse('the json status code is "{status_code}"'), target_fixture="context")
def check_json_status_code(context, status_code: str):
    assert context["response"].status_code == int(status_code)

    return context

@then(parsers.cfparse('the json response have title "{title}", synopsis "{synopsis}"'), target_fixture="context")
def check_response_json(context, title: str, synopsis: str):
    
    json_response = context["response"].json()
    assert json_response["title"] == title
    assert json_response["synopsis"] == synopsis

    return context


"""registrar filme com mesmo título"""
@scenario(scenario_name="Try to register a movie on the database with title that already exists", feature_name="../features/movies.feature")
def test_register_movie_same_title():
    db = getDB()
    clearDB(db)

@then(parsers.cfparse('the json response have message "{message}"'), target_fixture="context")
def check_json_status_code(context, message: str):
    assert context["response"].json()["detail"] == message

    return context

@then(parsers.cfparse('"{num_movies}" movies are in the database'), target_fixture="context")
def check_json_status_code(context, num_movies: str):
    db = getDB()

    assert len(db["movies"]) == int(num_movies)

    return context


"""GET movie by title"""
@scenario(scenario_name="get a movie by title on the database", feature_name="../features/movies.feature")
def test_get_movie_by_title():
    db = getDB()
    clearDB(db)

@given(parsers.cfparse('movie with title "{title}", synopsis "{synopsis}" is in the database'))
def mock_movie_service_creation(title: str, synopsis: str):
    ContentService.add_content(Movie(
        title=title, 
        synopsis=synopsis,
        gender="random gender",
        duration=0,
        release_year=0,
        director="random director",
        main_cast=[]
    ), "movies")

@when(
    parsers.cfparse('a GET request is sent to "{req_url}"'), 
    target_fixture="context"
)
def send_get_movie_request(client, context, req_url: str):

    response = client.get(req_url)
    
    context["response"] = response
    return context

"""GET movie by title that does not exist"""
@scenario(scenario_name="get a movie by title that does not exist on the database", feature_name="../features/movies.feature")
def test_get_movie_by_title_not_exist():
    db = getDB()
    clearDB(db)

"""update movie on the database"""
@scenario(scenario_name="Update a movie on the database", feature_name="../features/movies.feature")
def test_update_movie():
    db = getDB()
    clearDB(db)

@when(
    parsers.cfparse('a PUT request is sent to "{req_url}" with title "{title}", synopsis "{synopsis}"'), 
    target_fixture="context"
)
def send_post_movie_request(client, context, req_url: str, title: str, synopsis: str):

    response = client.put(
        req_url,
        json={
            "title": title,
            "synopsis": synopsis,
            "gender": "ação",
            "duration": 120,
            "release_year": 2022,
            "director": "Tarantino",
            "main_cast": ["The Rock", "Xuxa"],
            "banner": "banner.png"
        })
    
    context["response"] = response
    return context

@then(parsers.cfparse('movie with title "{title}" is in the database'), target_fixture="context")
def check_json_status_code(context, title: str):
    db = getDB()

    found = False
    for content in db["movies"]:
        if content["title"] == title:
            found = True

    assert found == True

    return context

"""update movie on the database"""
@scenario(scenario_name="Update a movie on the database", feature_name="../features/movies.feature")
def test_update_movie_not_exist():
    db = getDB()
    clearDB(db)

"""delete movie by title"""
@scenario(scenario_name="delete a movie by title on the database", feature_name="../features/movies.feature")
def test_delete_movie():
    db = getDB()
    clearDB(db)

@when(
    parsers.cfparse('a DELETE request is sent to "{req_url}"'), 
    target_fixture="context"
)
def send_get_movie_request(client, context, req_url: str):
    response = client.delete(req_url)
    
    context["response"] = response
    return context

"""delete movie by title that does not exist"""
@scenario(scenario_name="delete a movie by title that does not exist on the database", feature_name="../features/movies.feature")
def test_delete_movie_not_exist():
    db = getDB()
    clearDB(db)

"""get all movies"""
@scenario(scenario_name="get all movies in the database", feature_name="../features/movies.feature")
def test_get_all_movies():
    db = getDB()
    clearDB(db)

@then(parsers.cfparse('the json response have movie with title "{title}"'), target_fixture="context")
def check_response_json(context, title: str):    
    json_response = context["response"].json()

    assert type(json_response) == list
    found = False
    for element in json_response:
        if element["title"] == title:
            found = True
    
    assert found ==  True
    
    return context
