# microservice_backend

## Commands list:

##### Check code style before each new commit!

Run code style test:

`docker-compose -f docker-compose-dev.yml run users flake8 project`


Build the images:

`docker-compose -f docker-compose-dev.yml build`

Build & run the containers:

`docker-compose -f docker-compose-dev.yml up -d --build`

Recreate the database:

`docker-compose -f docker-compose-dev.yml run users python manage.py recreate_db`

Seed the database with initial values:

`docker-compose -f docker-compose-dev.yml run users python manage.py seed_db`

Run the tests:

`docker-compose -f docker-compose-dev.yml run users python manage.py test`

Run the tests with code coverage:

`docker-compose -f docker-compose-dev.yml run users python manage.py cov`

Stop the container:

`docker-compose -f docker-compose-dev.yml stop`

Stop and remove container:

`docker-compose -f docker-compose-dev.yml down`

Force a build

`docker-compose -f docker-compose-dev.yml build --no-cache`

Access PostgreSQL via psql?

`docker-compose -f docker-compose-dev.yml exec users-db psql -U [YOUR NAME: usually postgres or admin]`

## Endpoints:

`localhost:5001/users`: [GET] - get all users

`localhost:5001/users`: [POST] - add new user

`localhost:5001/users/[<id>]` [GET] - get user with id if exists

`localhost:5001/` [GET] - empty {}

`localhost:5001/users/ping` - [GET] - to check if application is on in case of DB problems

`localhost:3008/` - Swagger API, currently default example from swagger.io

## Data:
User:
* id (autoincrement, primary key)
* username
* email
* active (default True)

## Configs:
* Development
* Production
* Testing

## Flake8:
* 120 max line length
