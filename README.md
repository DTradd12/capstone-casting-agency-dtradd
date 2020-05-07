# Capstone Casting Agency
## Full Stack Nano Degree - Final Project

### About
This is the capstone project for Udacitys Full Stack Web Development Nano Degree. The goal of this project to
utilize all of the skills learned from the course and apply them to creating a full stack application.

The application follows the guidelines given for creating a casting agency that stores and delivers information on 
actors and movies.

####Live app hosted on Heroku:

https://capstone-casting-agency-dtradd.herokuapp.com/

### API
In order for a visitor to use the website, they must be authenticated. There are three seperate roles, with varying 
levels of permissions.

### Roles:
#### Casting Assistant
* GET: actors and movies

####Casting Director
* GET: actors and movies
* POST: actors 
* DELETE: actors
* PATCH: actors or movies

####Executive Producer
* GET: actors and movies
* POST: actors and movies
* DELETE: actors and movies
* PATCH: actors or movies


##Endpoint examples and behaviours.

**GET** `/actors`

Retrieves a list of all actors.

Minumum role required: Casting Assistant

``` 
curl -H "authorization: Bearer <YOUR TOKEN>" /
     -X GET https://capstone-casting-agency-dtradd.herokuapp.com/actors
```

**GET** `/movies`

Retrieves a list of all movies.

Minumum role required: Casting Assistant

``` 
curl -H "authorization: Bearer <YOUR TOKEN>" /
     -X GET https://capstone-casting-agency-dtradd.herokuapp.com/movies
```

**GET** `/actors/<id>`


Retrieves a specific actors data.

Minumum role required: Casting Assistant

``` 
curl -H "authorization: Bearer <YOUR TOKEN>" /
     -X GET https://capstone-casting-agency-dtradd.herokuapp.com/actors/<int>
```

**GET** `/movies/<id>`

Retrieves a specific movies data.

Minumum role required: Casting Assistant

``` 
curl -H "authorization: Bearer <YOUR TOKEN>" /
     -X GET https://capstone-casting-agency-dtradd.herokuapp.com/movies/<int>
```

**DELETE** `/actors/<id>`

Deletes a specific actor from the database.

Minumum role required: Casting Director

``` 
curl -H "authorization: Bearer <YOUR TOKEN>" /
     -X DELETE https://capstone-casting-agency-dtradd.herokuapp.com/actors/<int>
```

**DELETE** `/movies/<id>`

Deletes a specific movie from the database.

Minumum role required: Executive Producer

``` 
curl -H "authorization: Bearer <YOUR_TOKEN>" /
     -X DELETE https://capstone-casting-agency-dtradd.herokuapp.com/movies/<int>
```

**POST** `/actors/create`

Creates a new actor.

Minumum role required: Casting Director

```
curl -H "Content-Type: application/json" /
     -H "authorization: Bearer <YOUR_TOKEN>" /
     -d "{\"name\": \"Steve Carrell\", \"age\": 55, \"gender\":\"male\"}" /
     -X POST https://capstone-casting-agency-dtradd.herokuapp.com/actors/create
```

**POST** `/movies/create`

Creates a new movie.

Minumum role required: Executive Producer

```
curl -H "Content-Type: application/json" /
     -H "authorization: Bearer <YOUR_TOKEN>" /
     -d "{\"title\": \"Star Wars\", \"release_date\": \"May 18, 1980\"}" /
     -X POST https://capstone-casting-agency-dtradd.herokuapp.com/movies/create
```

**PATCH** `/actors/<id>`

Edits a specific actors data.

Minumum role required: Casting Director

```
curl -H "Content-Type: application/json" /
     -H "authorization: Bearer <YOUR_TOKEN>" /
     -d "{\"name\": \"Bruce Willis\"}" /
     -X PATCH https://capstone-casting-agency-dtradd.herokuapp.com/actors/<id>
```

**PATCH** `/movies/<id>`

Edits a specific movies data.

Minumum role required: Casting Director

```
curl -H "Content-Type: application/json" /
     -H "authorization: Bearer <YOUR_TOKEN>" /
     -d "{\"title\": \"The Sixth Sense\"}" /
     -X PATCH https://capstone-casting-agency-dtradd.herokuapp.com/movies/<id>
```

##Installation
###Dependencies

```
OPTIONAL:python -m venv env
OPTIONAL:env/bin/activate
pip install -r requirements.txt
```

### Database Setup

Log into your database with psql commands.

```
psql -U <username> -p <port>
Enter password when prompted
```
Once logged in:
```
create database castingagency;
```

### Running the Server Locally

The following environment variables must be set:
```
set FLASK_APP=APP
set FLASK_ENV=development
set FLASK_DEBUG=true
```

## Unit Tests

In order to run the unit tests within the repo, the following steps must be taken.
* Create a test database named 'castingagency_test'.
* Run the following file with Python.
```python test_app.py```
