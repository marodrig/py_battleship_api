# py_battleship_api
Django application implementing a basic REST API for battleship.

## Table of Contents
1. [Features](#features)

2. [Prerequisites](#prerequisites)

3. [Getting Started](#getting-started)

4. [Usage](#usage)

5. [Running Tests](#running-tests)

6. [Built With](#built-with)

7. [License](#license)

## Features

A RESTful API for a one player game of battleship.  It includes the ability to randomize the starting location of oponents ships.

## Prerequisites

- Python 3.5.2
- Django.
- Pip for managing Python Packages.
- Coverage.py for checking test coverage of code.
- virtualenv to separte our development environment and Python version from other projects.

## Getting Started

### Python

We need python version 3.x.x

### PIP

Once we have installed pip, we can install the requirements by typing:

```
pip install -r requirements.txt
```

### Virtualenv

A more detail guide of how to setup virtualenv for our enviroment can be found in the following link:

[https://packaging.python.org/guides/installing-using-pip-and-virtualenv/](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/)
## Usage

The API endpoints response are in JSON format.

|                       API end point       |      GET method                      |    POST method      |
|-------------------------------------------|--------------------------------------|---------------------|
|/battleship/api/v1/games/                  | N/A                                  | Creates a new game  |
|/battleship/api/v1/games/<int:game_id>/ships| N/A                                 | Randomly places five ships of different types in a 10x10 board |
|/battleship/api/v1/games/<int:game_id>     | Return information about the game    | N/A                 |
|/battleship/api/v1/games/<int:game_id>/shot?row=1&column=1     | Launches a torpedo at location row, column   | N/A|

### Data base migration

This project uses a sqlite3 database. You will need to create and migrate the schema using django's migration tool.
```
python manage.py makemigrations
```

```
python manage.py migrate
```

The database has been setup.

### Running server locally

The current settings are set for port 8000 on localhost.  You can start the server by typing:

```
python manage.py runserver
```

### Running Tests

### Testing coverage of unit tests

We can use coverage.py to check how much of our code has been tested by our unit tests.  First we need to run our tests using coverage by typing the following on the prompt:

```
coverage run --source='.' manage.py test battleship_api
```

To read the report of the break down of our unit test coverage we can do so by typing the following commands:

```
coverage report
```

## Deployment

## Built with

## License
