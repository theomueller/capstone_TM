# CAPTSONE Backend

"CAPSTONE backend" is a first implementation of a backend which proposes an API service to cover the needs of a casting agency. The goal is to manage movies and actors. The database saves the information which actors played in which film as JOIN table.

The server is running on heroku as the address: https://capstonetm.herokuapp.com/

There are three different roles:

- Casting Assistant
  can view actors and movies
- Casting Director
  can view actors and movies
  can add or delete an actor from the database
  can modify actors or movie
- Executive Producer
  can view actors and movies
  can add or delete actors and movies from the database
  can modify actors or movie

### Backend

The `./backend/src` directory contains a partially completed Flask server with a pre-written SQLAlchemy module. Some endpoints are already configured and integrated Auth0 for authentication.

## Getting Started

The backend is developed with FLASK und used a postgresql database. The app is deployed in heroku with the gunicorn as server.

### Installing Dependencies

#### Python 3.9

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

```bash
python3 -m venv venv
source venv/bin/activate
```

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend/src` directory and running:

```bash
pip3 install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

ATTENTION: it is necessary to install an old version of SQLAlchemy to be able to use sqlite
Version before 1.4 or after 2.4 are fine !

- [jose] JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

python3 manage.py db init
python3 manage.py db migrate
python3 manage.py db upgrade

Each time you open a new terminal session, run:

```bash
source setup.sh
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

### Best practice

the code adheres as far as possible to the PEP8 Style Guide
-> checked were app.py and models.py

### Descrption repo

app.py: main program with the creation of the app and the definition of the routes
auth.py: module to handle the autorisation (permissions). The authorization is performed with auth0 service. The link to registration is https://capstone-theo.eu.auth0.com to get the tokens.
captsone.postman_test:run.json: the results of the tests and the api calls saved in a collection in postmann. Host can be changed to your localhost if needed.
manage.py: module to handle the database. use python db manage upgrade to start
models.py: description of the tables for the database
Procfile: config to define the web server in heroku
README_backend.md: this file :-)
requirements.txt: see above in PIP Dependencies
setup.sh: config file with the database_url, client_id, tokens
test_apppy: unit test

### Description API

Postmann was used to test the API. A collection is available in the repo and the documentation is published on the web: https://documenter.getpostman.com/view/9891951/TzzHksev

The corresponding routes and call with curl are available.

The api can be tested with test_app.py. The same db was used for the tests as during development. It would be wise to use an other instance.

### API Errors:

Defined Error handlers:

- 400 - Bad reqest
- 401 - token expired / invalid claims / invalid header
- 403 - unauthorized
- 404 - Resource not found
- 405 - method not allowed
- 422 - Unprocessable entity
- 500 - Internal Server error

Example of retour from a bad call:

```json
{
  "error": 422,
  "message": "unprocessable",
  "success": false
}
```

### Next steps and to dos

- implement the CRUD Methods for the joined table "ROLE"
- extends the fields of the tables
- implements a front end to consume the api

Good luck and enjoy the api
