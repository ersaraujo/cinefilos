from src.db.database import getDB, saveDB, clearDB
from pytest_bdd import parsers, given, when, then, scenario
from src.service.impl.content_service import ContentService
from src.schemas.content import TvShow

@scenario(scenario_name="Register a tv show on the database", feature_name="../features/tv_shows.feature")
def test_register_tv_show():
    db = getDB()
    clearDB(db)

@given(parsers.cfparse('no tv show with title "{title}" is in the database'))
def mock_tv_show_service_clean(title: str):
    pass

@when(
    parsers.cfparse('a POST request is sent to "{req_url}" with title "{title}", synopsis "{synopsis}"'), 
    target_fixture="context"
)
def send_post_tv_show_request(client, context, req_url: str, title: str, synopsis: str):

    response = client.post(
        req_url,
        json={
            "title": title,
            "synopsis": synopsis,
            "gender": "ação",
            "num_seasons": 12,
            "num_episodes": 200,
            "release_year": 2001,
            "creator": "Tarantino",
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
@scenario(scenario_name="Try to register a tv show on the database with title that already exists", feature_name="../features/tv_shows.feature")
def test_register_tv_show_same_title():
    db = getDB()
    clearDB(db)

@then(parsers.cfparse('the json response have message "{message}"'), target_fixture="context")
def check_json_status_code(context, message: str):
    assert context["response"].json()["detail"] == message

    return context

@then(parsers.cfparse('"{num_tv_shows}" tv shows are in the database'), target_fixture="context")
def check_json_status_code(context, num_tv_shows: str):
    db = getDB()

    assert len(db["tv_shows"]) == int(num_tv_shows)

    return context


"""GET tv_show by title"""
@scenario(scenario_name="get a tv show by title on the database", feature_name="../features/tv_shows.feature")
def test_get_tv_show_by_title():
    db = getDB()
    clearDB(db)

@given(parsers.cfparse('tv show with title "{title}", synopsis "{synopsis}" is in the database'))
def mock_tv_show_service_creation(title: str, synopsis: str):

    ContentService.add_content(TvShow(
        title=title, 
        synopsis=synopsis,
        gender="random gender",
        num_seasons=12,
        num_episodes=120,
        release_year=0,
        creator="random director",
        main_cast=[]
    ), "tv_shows")

@when(
    parsers.cfparse('a GET request is sent to "{req_url}"'), 
    target_fixture="context"
)
def send_get_tv_show_request(client, context, req_url: str):

    response = client.get(req_url)
    
    context["response"] = response
    return context

"""GET tv_show by title that does not exist"""
@scenario(scenario_name="get a tv show by title that does not exist on the database", feature_name="../features/tv_shows.feature")
def test_get_tv_show_by_title_not_exist():
    db = getDB()
    clearDB(db)

"""update tv_show on the database"""
@scenario(scenario_name="Update a tv show on the database", feature_name="../features/tv_shows.feature")
def test_update_tv_show():
    db = getDB()
    clearDB(db)

@when(
    parsers.cfparse('a PUT request is sent to "{req_url}" with title "{title}", synopsis "{synopsis}"'), 
    target_fixture="context"
)
def send_post_tv_show_request(client, context, req_url: str, title: str, synopsis: str):

    response = client.put(
        req_url,
        json={
            "title": title,
            "synopsis": synopsis,
            "gender": "ação",
            "num_seasons": 12,
            "num_episodes": 200,
            "release_year": 2022,
            "creator": "Tarantino",
            "main_cast": ["The Rock", "Xuxa"],
            "banner": "banner.png"
        })
    
    context["response"] = response
    return context

@then(parsers.cfparse('tv show with title "{title}" is in the database'), target_fixture="context")
def check_json_status_code(context, title: str):
    db = getDB()

    found = False
    for content in db["tv_shows"]:
        if content["title"] == title:
            found = True

    assert found == True

    return context

"""update tv_show on the database"""
@scenario(scenario_name="Update a tv show on the database", feature_name="../features/tv_shows.feature")
def test_update_tv_show_not_exist():
    db = getDB()
    clearDB(db)

"""delete tv_show by title"""
@scenario(scenario_name="delete a tv show by title on the database", feature_name="../features/tv_shows.feature")
def test_delete_tv_show():
    db = getDB()
    clearDB(db)


@when(
    parsers.cfparse('a DELETE request is sent to "{req_url}"'), 
    target_fixture="context"
)
def send_get_tv_show_request(client, context, req_url: str):
    response = client.delete(req_url)
    
    context["response"] = response
    return context

"""delete tv_show by title that does not exist"""
@scenario(scenario_name="delete a tv show by title that does not exist on the database", feature_name="../features/tv_shows.feature")
def test_delete_tv_show_not_exist():
    db = getDB()
    clearDB(db)

"""get all tv_shows"""
@scenario(scenario_name="get all tv shows in the database", feature_name="../features/tv_shows.feature")
def test_get_all_tv_shows():
    db = getDB()
    clearDB(db)

@then(parsers.cfparse('the json response have tv show with title "{title}"'), target_fixture="context")
def check_response_json(context, title: str):    
    json_response = context["response"].json()

    assert type(json_response) == list
    found = False
    for element in json_response:
        if element["title"] == title:
            found = True
    
    assert found ==  True
    
    return context

