Feature: Tv Shows API

    Scenario: Register a tv show on the database
        Given no tv show with title "Os Simpsons" is in the database
        When a POST request is sent to "/contents/tv_shows" with title "Os Simpsons", synopsis "Uma família americana comum, com todo mundo é amarelo"
        Then the json status code is "201"
        And the json response have title "Os Simpsons", synopsis "Uma família americana comum, com todo mundo é amarelo"

    Scenario: Try to register a tv show on the database with title that already exists
        Given tv show with title "Os Simpsons", synopsis "Uma família americana comum, com todo mundo é amarelo" is in the database
        When a POST request is sent to "/contents/tv_shows" with title "Os Simpsons", synopsis "Uma família americana comum, com todo mundo é amarelo"
        Then the json status code is "422"
        And the json response have message "There is a tv show with the same title in the database"
        And "1" tv shows are in the database

    Scenario: get a tv show by title on the database
        Given tv show with title "Os Simpsons", synopsis "Uma família americana comum, com todo mundo é amarelo" is in the database
        When a GET request is sent to "/contents/tv_shows/Os%20Simpsons"
        Then the json status code is "200"
        And the json response have title "Os Simpsons", synopsis "Uma família americana comum, com todo mundo é amarelo"

    Scenario: get a tv show by title that does not exist on the database 
        Given no tv show with title "Os Simpsons" is in the database
        When a GET request is sent to "/contents/tv_shows/Os%20Simpsons"
        Then the json status code is "404"
        And the json response have message "No tv show with this title found in the database"

    Scenario: Update a tv show on the database
        Given tv show with title "Os Simpsons", synopsis "Uma família americana comum, com todo mundo é amarelo" is in the database
        When a PUT request is sent to "/contents/tv_shows/Os%20Simpsons" with title "Friends", synopsis "Amigos com histórias divertidas e inusitadas"
        Then the json status code is "200"
        And the json response have title "Friends", synopsis "Amigos com histórias divertidas e inusitadas"
        And "1" tv shows are in the database
        And tv show with title "Friends" is in the database

    Scenario: Try to update a tv show on the database with title that does not exist
        Given tv show with title "Os Simpsons", synopsis "Uma família americana comum, com todo mundo é amarelo" is in the database
        When a PUT request is sent to "/contents/tv_shows/Friends" with title "Friends", synopsis "Amigos com histórias divertidas e inusitadas"
        Then the json status code is "404"
        And the json response have message "No tv show with this title found in the database"
        And "1" tv shows are in the database
        And tv show with title "Os Simpsons" is in the database

    Scenario: delete a tv show by title on the database
        Given tv show with title "Os Simpsons", synopsis "Uma família americana comum, com todo mundo é amarelo" is in the database
        And tv show with title "Friends", synopsis "Amigos com histórias divertidas e inusitadas" is in the database
        When a DELETE request is sent to "/contents/tv_shows/Os%20Simpsons"
        Then the json status code is "200"
        And the json response have title "Os Simpsons", synopsis "Uma família americana comum, com todo mundo é amarelo"
        And "1" tv shows are in the database
        And tv show with title "Friends" is in the database

    Scenario: delete a tv show by title that does not exist on the database 
        Given tv show with title "Os Simpsons", synopsis "Uma família americana comum, com todo mundo é amarelo" is in the database
        When a DELETE request is sent to "/contents/tv_shows/Matrix"
        Then the json status code is "404"
        And the json response have message "No tv show with this title found in the database"
        And "1" tv shows are in the database
        And tv show with title "Os Simpsons" is in the database

    Scenario: get all tv shows in the database
        Given tv show with title "Os Simpsons", synopsis "Uma família americana comum, com todo mundo é amarelo" is in the database
        And tv show with title "Matrix", synopsis "Uma distopia cheia de mistérios e grandes revelações", gender "ação", duration "150", release year "2008", director "Tarantino", main cast "Bart, Lisa, Homer", banner "matrix.png" is in the database
        When a GET request is sent to "/contents/tv_shows"
        Then the json status code is "200"
        And the json response have tv show with title "Os Simpsons"
        And the json response have tv show with title "Matrix"