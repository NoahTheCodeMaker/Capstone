# This is a Repository for the Udacity FSND Capstone Project

## ^^ Which I passed with flying colors on my first attempt!

# See my React Capstone Frontend at https://github.com/NoahTheCodeMaker/React-Frontend-Test where I created a frontend for this app in React.js

## Motivation for this project

  As I went with the standard Udacity outline for this project, you may think that I was not feeling very 
  motivated for this project. I assure you that this is not the case! I started this Udacity nanodegree 
  program just before going back to school for my final semester to get my degree in Science, Technology, 
  and Mathematics with studies in Computer Science. Because of this, I fell behind in the course, and was 
  always bothered by the slow pace that I was going. As I now have my degree, I wanted to get this project 
  done as soon as possible (also because this is also an expensive course to be activity enrolled in), 
  and I actually completed this project in only 3 days, my shortest time taken on a project yet!

### See the Getting Started section of the API Documentation for the Hosted URL of my API!

## Dependencies

  This API is run with Flask, Flask-CORS and Flask-SQLAlchemy. 
  It uses Postgresql and psycopg2 for the database and database interactions.
  The Authorization is handled by Auth0 and with the python-jose library for decoding JWTs
  This web app uses Gunicorn to run in production.


## Running Locally

  To run this project on your machine, you will need to use the command "source setup.sh" 
  after uncommenting all of the local environment variables, as these are needed to run.
  After running this command, the dependencies will be installed, the environment variables 
  will be set, and the database will be completely set up (under the default postgres database).
  Then, all you have to do is use the command "flask run" and the API will be up and ready!

## Hosting Instructions

  I am having this app hosted by render cloud platform as of writing. Just setting the "source setup.sh" 
  command without uncommenting the local environment variables and setting the proper environment variables 
  in the app settings is all that needs to be done for this app to be hosted on render!


## Testing

  To make the testing very easy, I created a script - test.sh - for the Udacity reviewers. This script 
  fully sets up the database under the default postgres user with some starter information. Then, 
  it automatically runs all of the tests. (For the Udacity Reviewers) See this script for more information.

# API Documentation

## API Introduction

  This project is for a Casting Agency conveniently called noahdragoonudacitycapstone. The API in this project is 
  responsible for creating movies and managing and assigning actors to those movies. This project streamlines this process.

## Getting Started

  This API is hosted by the render cloud platform at https://noahdragoonudacitycapstone.onrender.com/

  There are no API Keys, but there is Authentication by Auth0. See the below description for this. 

## Authentication

  I created a /login endpoint and a /auth endpoint for anybody who wants to attempt a login and use the 
  JWT received by /login by sending it to the /auth endpoint which will only work if your user is valid 
  and will send back the payload of the JWT. This endpoint expects an Authorization
  header with a bearer token containing a valid JWT, no permissions are needed for this endpoint.

  Here are the roles describing permissions for this API
  ```
  Roles:
  Casting Assistant
    Can view actors and movies
  Casting Director
    All permissions a Casting Assistant has and…
    Add or delete an actor from the database
    Modify actors or movies
  Executive Producer
    All permissions a Casting Director has and…
    Add or delete a movie from the database
  ```

  For Udacity Reviewers, I have included the tokens.py file with the following JWT tokens for usage in testing, 
  which you can also use (for as long as they are valid).

  ```
  An EXPIRED_TOKEN for testing failure.
  A CASTING_ASSISTANT_TOKEN for testing the casting assistant role.
  A CASTING_DIRECTOR_TOKEN for testing the casting director role.
  An EXECUTIVE_PRODUCER_TOKEN for testing the executive producer role.
  ```

  Without this file, the test_app will fail the RBAC tests, which most tests are.

  See the request arguments in the API Resource Endpoint Library to see what endpoints require which permissions.

## Error Messages

The error codes 400, 404, 405, 422, and 500 are the error codes most expected to occur in this app.
Keeping this in mind, here are the returned json responses for each code so you can expect them.

```
Response for Error Code 400
{
  "success": False,
  "error": 400,
  "message": "bad request"
} 
Response for Error Code 404
{
  "success": False,
  "error": 404,
  "message": "resource not found"
}
Response for Error Code 405
{
  "success": False,
  "error": 405,
  "message": "method not allowed"
}
Response for Error Code 422
{
  "success": False,
  "error": 422,
  "message": "unprocessable entity"
}
Response for Error Code 500
{
  "success": False,
  "error": 500,
  "message": "internal server error"
}
```

  If the error is because of Authentication problems, the json responses will have an object with 
  "code" and "description"keys under the "message" key. This will only occur with 400, 401, and 403.
  See the example below for an example of this.

```
{
    "error": 401,
    "message": {
        "code": "authorization_header_missing",
        "description": "Authorization header is expected."
    },
    "success": false
}
```
## API Resource Endpoint Library

  I will be using the hosted API URL for the examples, 
  but if running locally, you can switch out the hosted URL for http://127.0.0.1:5000

```
All Endpoints
GET '/'
GET '/login'
GET '/auth'
GET '/actors'
GET '/movies'
POST '/actors'
POST '/movies'
PATCH '/actors'
PATCH '/movies'
DELETE '/actors'
DELETE '/movies'

Endpoint Descriptions in order of list above
GET '/'
- Gives the user a welcome message
- Request Arguments: None
- Returns: See example response below, this is static.
- Example Request: curl https://noahdragoonudacitycapstone.onrender.com/
- Example Response: 
{
  "success": True,
  "message": "Welcome to my Capstone Project! Please navigate to /login to log into an account!"
}

GET '/login'
- Redirects the user to the hosted Auth0 login page
- Request Arguments: None
- Returns: None
- Example Request: curl https://noahdragoonudacitycapstone.onrender.com/login
- Example Response: None

GET '/auth'
- Takes a JWT and returns the payload if it is a valid JWT from the apps Auth0 login
- Request Arguments: Expects a bearer token in header under key 'Authorization', no permissions needed, just a valid JWT bearer
- Returns: Decoded and parsed "payload" object from JWT provided which includes user permissions, and a "success" key with a boolean indicating success
- Example Request: curl -H 'Authorization: Bearer {Token_ID_Here}' https://noahdragoonudacitycapstone.onrender.com/auth
- Example Response: 
{
  "payload": {
    "aud": "https://NoahCapstone",
    "azp": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "exp": 1678707679,
    "iat": 1678621279,
    "iss": "https://dev-y4dtlj6thn26xy28.us.auth0.com/",
    "permissions": [
      "create:actors",
      "create:movies",
      "delete:actors",
      "delete:movies",
      "edit:actors",
      "edit:movies",
      "read:actors",
      "read:movies"
    ],
    "scope": "",
    "sub": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  },
  "success": true
}

GET '/actors'
- Endpoint for looking up all of the actors in the database.
- Request Arguments: Expects a bearer token in header under key 'Authorization' with the read actors permission
- Returns: An "actors" key with all of the actor objects in the database, and a "success" key with a boolean indicating success
- Example Request: curl -H 'Authorization: Bearer {Token_ID_Here}' https://noahdragoonudacitycapstone.onrender.com/actors
- Example Response:
{
    "actors": [
        {
            "age": 50,
            "gender": "Male",
            "id": 1,
            "name": "Dwayne 'The Rock' Johnson"
        },
        {
            "age": 48,
            "gender": "Female",
            "id": 2,
            "name": "Drew Barrymore"
        },
        {
            "age": 56,
            "gender": "Male",
            "id": 3,
            "name": "Adam Sandler"
        }
    ],
    "success": true
}

GET '/movies'
- Endpoint for looking up all of the movies in the database.
- Request Arguments: Expects a bearer token in header under key 'Authorization' with the read movies permission
- Returns: A "movies" key with all of the movie objects in the database, and a "success" key with a boolean indicating success
- Example Request: curl -H 'Authorization: Bearer {Token_ID_Here}' https://noahdragoonudacitycapstone.onrender.com/movies
- Example Response: 
{
    "movies": [
        {
            "id": 1,
            "release_date": "May 29th, 2015",
            "title": "San Andreas"
        },
        {
            "id": 2,
            "release_date": "May 23rd, 2014",
            "title": "Blended"
        },
        {
            "id": 3,
            "release_date": "June 25th, 2010",
            "title": "Grown Ups"
        }
    ],
    "success": true
}

POST '/actors'
- Endpoint that creates an actor in the database
- Request Arguments: Expects a bearer token in header under key 'Authorization' with the create actors permission as well as the data header 'Content-Type: application/json'. 
Also expects the following arguments in the body "name" containing a string name, "age" containing an integer, and "gender" containing a gender string.
- Returns: The created "actor" object, and a "success" key with a boolean indicating success
- Example Request: curl -d '{"name":"Drew Barrymore", "age":48, "gender":"Female"}' -H 'Authorization: Bearer {Token_ID_Here}' -H 'Content-Type: application/json' -X POST https://noahdragoonudacitycapstone.onrender.com/actors
- Example Response: 
{
    "actor": {
        "age": 48,
        "gender": "Female",
        "id": 2,
        "name": "Drew Barrymore"
    },
    "success": true
}

POST '/movies'
- Endpoint that creates a movie in the database
- Request Arguments: Expects a bearer token in header under key 'Authorization' with the create movies permission as well as the data header 'Content-Type: application/json'. 
Also expects the following arguments in the body "title" containing a string title, and "release_date" containing a date string.
- Returns: The created "movie" object, and a "success" key with a boolean indicating success
- Example Request: curl -d '{"title":"San Andreas", "release_date":"May 29th, 2015"}' -H 'Authorization: Bearer {Token_ID_Here}' -H 'Content-Type: application/json' -X POST https://noahdragoonudacitycapstone.onrender.com/movies
- Example Response: 
{
    "movie": {
        "id":1,
        "release_date":"May 29th, 2015",
        "title":"San Andreas"
      },
    "success":true
}

PATCH '/actors'
- Updates the actor with new age, gender, or name information using the id
- Request Arguments: Expects a bearer token in header under key 'Authorization' with the edit actors permission as well as the data header 'Content-Type: application/json'. 
Also expects the following arguments in the body "id" containing the id of the actor to edit, "name" containing a string name, "age" containing an integer, and "gender" containing a gender string.
- Returns: The updated actor object and a "success" key with a boolean indicating success
- Example Request: curl -d '{"id":1,"name":"Jason Statham", "age":55, "gender":"Male"}' -H 'Authorization: Bearer {Token_ID_Here}' -H 'Content-Type: application/json' -X PATCH https://noahdragoonudacitycapstone.onrender.com/actors
- Example Response: 
{
    "actor": {
        "age": 55,
        "gender": "Male",
        "id": 1,
        "name": "Jason Statham"
    },
    "success": true
}

PATCH '/movies'
- Updates the movie with new age, gender, or name information using the id
- Request Arguments: Expects a bearer token in header under key 'Authorization' with the edit movies permission as well as the data header 'Content-Type: application/json'. 
Also expects the following arguments in the body "id" containing the id of the movie to edit, "title" containing a string title, and "release_date" containing a date string.
- Returns: The updated movie object and a "success" key with a boolean indicating success
- Example Request: curl -d '{"id":1, "title":"The Meg", "release_date":"August 10th, 2018"}' -H 'Authorization: Bearer {Token_ID_Here}' -H 'Content-Type: application/json' -X PATCH https://noahdragoonudacitycapstone.onrender.com/movies
- Example Response: 
{
    "movie": {
        "id": 1,
        "release_date": "August 10th, 2018",
        "title": "The Meg"
    },
    "success": true
}

DELETE '/actors'
- Deletes the actor using the id
- Request Arguments: Expects a bearer token in header under key 'Authorization' with the delete actors permission as well as the data header 'Content-Type: application/json'.
Also expects the "id" argument in the body containing the id of the actor to delete
- Returns: The "deleted_actor_id" containing the id as an integer of the actor deleted, and a "success" key with a boolean indicating success
- Example Request: curl -d '{"id":1}' -H 'Authorization: Bearer {Token_ID_Here}' -H 'Content-Type: application/json' -X DELETE https://noahdragoonudacitycapstone.onrender.com/actors
- Example Response: 
{
    "deleted_actor_id":1,
    "success":true
}

DELETE '/movies'
- Deletes the movie using the id
- Request Arguments: Expects a bearer token in header under key 'Authorization' with the delete movies permission as well as the data header 'Content-Type: application/json'.
Also expects the "id" argument in the body containing the id of the movie to delete
- Returns: The "deleted_movie_id" containing the id as an integer of the movie deleted, and a "success" key with a boolean indicating success
- Example Request: curl -d '{"id":1}' -H 'Authorization: Bearer {Token_ID_Here}' -H 'Content-Type: application/json' -X DELETE https://noahdragoonudacitycapstone.onrender.com/movies
- Example Response: 
{
    "deleted_movie_id":1,
    "success":true
}
```
