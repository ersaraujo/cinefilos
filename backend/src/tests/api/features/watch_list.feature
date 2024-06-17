Feature: Watch List API

    Scenario: Add movie to category
        Given no movie with title "Duna 2" is in the "assistidos" list of the user "Gusta"
        And movie with title "Duna 2", content_id "d7930544" is in the database
        When a POST request is sent to the list "assistidos" of the user "Gusta", content_id "d7930544"
        Then the json status code is "201"
        And the json response have title "Duna 2", content_id "d7930544"

    Scenario: Add movie that is already in category
        Given movie with title "Duna", content_id "d7930544-2f92-471d-86d1-48c463fbff85" is in the database
        And movie with title "Duna" is in the "assistidos" list of the user "Gusta"
        When a POST request is sent to the list "assistidos" of the user "Gusta", content_id "d7930544-2f92-471d-86d1-48c463fbff85"
        Then the json status code is "422"
        And the json response have message "This movie is already in the category"

    Scenario: Add movie that is not in database to category
        Given no movie with title "Duna 3" is in the database
        When a POST request is sent to the list "assistidos" of the user "Gusta", content_id "48c463fbff85"
        Then the json status code is "404"
        And the json response have message "No movie with this ID found in the database"

    Scenario: Get movie from category list
        Given movie with title "Duna", content_id "d7930544-2f92-471d-86d1-48c463fbff85" is in the database
        And movie with title "Duna" is in the "assistidos" list of the user "Gusta"
        When a GET request is sent to the list "assistidos" of the user "Gusta"
        Then the json status code is "200"
        And the json response contains the movie with title "Duna"

    Scenario: Get category list
        Given user with username "Gusta" is in the database
        When a GET request is sent to the list "assistidos" of the user "Gusta"
        Then the json status code is "200"
        And the json response contains a items_list
    
    Scenario: Remove movie from category
        Given movie with title "Duna", content_id "d7930544-2f92-471d-86d1-48c463fbff85" is in the database
        And movie with title "Duna" is in the "assistidos" list of the user "Gusta"
        When a DELETE request is sent to the list "assistidos" of the user "Gusta", content_id "d7930544-2f92-471d-86d1-48c463fbff85"
        Then the json status code is "200"
        And the json response have title "Duna", content_id "d7930544-2f92-471d-86d1-48c463fbff85"
        
    Scenario: Remove movie not in the category
        Given no movie with title "Duna 3" is in the "assistidos" list of the user "Gusta"
        When a DELETE request is sent to the list "assistidos" of the user "Gusta", content_id "d7930544-2f92-471d"
        Then the json status code is "404"
        And the json response have message "No movie with this ID found in this category"
