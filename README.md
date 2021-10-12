# Full Stack Capstone Project


## Full Stack Casting Agency

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. The idea is to create a webpage and an API to simplify and streamline the process for the Executive Producer.


Creating this Casting Agency app gave me the ability to structure plan, implement, and test an API - skills essential for enabling my future applications to communicate with others.
## Getting started
### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip and node installed on their local machines.

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file. 

To run the application run the following commands: 
```
export FLASK_APP=myapp 
FLASK_ENV=development
python3 app.py   
```

These commands put the application in development and directs our application to use the `app.py` file. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

#### Frontend

Frontend is not implemented yet.

### Tests
In order to run tests navigate to the backend folder and run the following commands: 

```
source setup.sh
dropdb casting_agency_test
createdb casting_agency_test
psql casting_agency_test < casting_agency.psql
python test_app.py
```
The three role access tokens should be provided in setup.sh file for the test
The first time you run the tests, omit the dropdb command. 

All tests are kept in that file and should be maintained as updates are made to app functionality. 


## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return four error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 
- AuthError 

### Endpoints 
#### GET /movies

- General:
    - Returns a list of movie objects , success value. 
- Sample: `curl http://127.0.0.1:5000/movies`

```
{
    "movies": [
        {
            "actors": [
                "Carey Mulligan",
                "Leonardo DiCaprio"
            ],
            "id": 1,
            "release_date": "Wed 05, 01, 2013 ",
            "title": "The great gatspy"
        },
        {
            "actors": [
                "Joel Fry",
                "Emma Stone"
            ],
            "id": 2,
            "release_date": "Thu 05, 27, 2021 ",
            "title": "Cruella"
        },
    ],
  "success": true
}
```
#### GET /actors
- General:
    - Returns a list of actor objects and success value.
- Sample: `curl http://127.0.0.1:5000/actors`

```
{
    "actors": [
        {
            "age": 36,
            "gender": "female",
            "id": 2,
            "name": "Carey Mulligan"
        },
        {
            "age": 36,
            "gender": "male",
            "id": 3,
            "name": "Joel Fry"
        },
        {
            "age": 32,
            "gender": "female",
            "id": 5,
            "name": "Emma Stone"
        },
        {
            "age": 46,
            "gender": "male",
            "id": 6,
            "name": "Leonardo DiCaprio"
        }
    ],
    "success": true
}
```

#### DELETE /movies/{movie_id}
- General:
    - Deletes the movie of the given ID if it exists. Returns the id of the deleted question, success value. 
- `curl -X DELETE http://127.0.0.1:5000/movies/16`

```
  "deleted": 1,
  "success": true,
}
```


#### POST /movies

- General:
    - Creates a new movie with title and release date. Returns the id of the created movie, success value. 

- `curl http://127.0.0.1:5000/movies -X POST -H "Content-Type: application/json" -d '{"title":"This is a movie", "release_date":" 05, 01, 2021 "}'`

```
{
    "movies": {
        "actors": [],
        "id": 20,
        "release_date": "Mon 05, 01, 2023 ",
        "title": "This is a movie"
    },
    "success": true
}
```

#### PATCH /movies/{movie_id}
- Sends a patch request in order to modify the movie record
- Returns a single new movie object and sucess value
``` 
{
    "movie": {
        "actors": [],
        "id": 20,
        "release_date": "Mon 05, 01, 2023 ",
        "title": "The new title"
    },
    "success": true
}
```

## Roles and Permissions

### Casting Assistant
- Can view actors and movies

### Casting Director
- All permissions a Casting Assistant has and…
- Add or Modify movies

### Executive Producer
- All permissions a Casting Director has and…
- delete a movie from the database

## Deployment N/A

## Authors
Maymonah Althunayan

## Acknowledgements 
So proud to graduate finish my last FSND project!

