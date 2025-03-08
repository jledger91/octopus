# Octopus Electroverse - Tech Task Template

## What is this project?
This project contains a basic containerised Python Django application that can be used as a starter
template to help you complete the tech task. 
Usage of this template project is completely optional, but should free up some time for
you to focus on the required domain logic.
It contains:
- A basic Django application.
- A Dockerfile to build the application.
- A docker-compose file to run the application.
- A requirements.txt file to install the required dependencies.
- This README.md file to help you get started, and act as a place to store your task notes.
- A Makefile containing helpful commands.
- A template Python .gitignore file.

## Quickstart
### Prerequisites
This project uses docker and docker compose. Ensure these are installed before
proceeding. The following setup has been tested using `Docker version 26.0.0`
and `docker-compose version 2.26.1`. This project uses a `Makefile` so 
please also ensure that `make` is installed on your machine.

A few of the usual `python manage.py` Django commands are proxied via `make` commands.
As an example of interacting with Django command, running Django migrations can be done via `make migrate ...`. Running Django shell will be `make shell ...`. 
You can find all the available commands in the `Makefile` within the top level directory.
Additional arguments may be provided to some commands by providing the `ARGS=""` parameter to the `make` command.

### How do I run the project locally?
* Run `make build` to build the container(s) needed. 
* Run `make up` to start the Django application and any dependent services defined in the compose file. 
* Run `make manage ARGS="migrate"` to prepare the database (this runs Django's `python manage.py ${ARGS}` command inside the container). This can be run in another shell window if you didn't run `make up` with the `ARGS="--detach"` flag.
* You'll need a user to log into the admin console. To create an admin user for the project run `make manage ARGS="createsuperuser"`.
* You should now be able to access the Django admin console from `http://localhost:8000/admin`, and a "Hello, world" page at `http://localhost:8000/task`

### Useful development commands
 - `make up` - start the application
 - `make down` - stop the application
 - `make test` - run the test suite
 - `make prep` - run code formatting and linting tools: `black`, `isort`, `mypy`, `lint`. These can also be run individually with the corresponding make command.

### Examples
- Rebuild and re-run the application in detached mode: `make up ARGS="--build --detach"`
- Running a specific test file: `make test ARGS="path/to/test.py"`
- Running tests matching a keyword: `make test ARGS="-k test_specific_test_case"`

## Solution Notes

### MVP
Initial bullet points (to expand on later!). I have:
- Modified settings to include the task app.
- Added django-extensions for shell_plus when playing with data importing.
- Created a management command to import and process the data.
- Created model to persist the data.
- Created REST views/serializers to expose this data.
- Written tests for the above.
- Added the data to my local root directory, so it would be on the volume for the container to access.
- Added said data folder to the .gitignore.
- (Manually tested as I went - the command through Docker and the views with cURL.)

### Getting serious
Initial bullet points. I have:
- Added a TimeStampedModel base for the Location model, so we can filter later by created/updated.
- Added the django_filters library.
- Created a simple filter set for the locations view (pausing the proximity ordering for later).
- Registered the relevant models on the Django admin.
- Updated the Country model Meta so that it doesn't present as "Countrys".
- Done some discovery on GeoDjango to understand how best to implement the proximity ordering.
- Attempted to migrate the coordinates field to a PointField (which I couldn't get to work in time).
