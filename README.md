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
Placing thoughts I had on the task in this section! I time-boxed myself to the four hours and managed to get most of the
way through the second stage, with some caveats that I'll dig into.

You can also find TODOs in the code with thoughts I have about more granular aspects.

### MVP
For the first section, I took a look at the expected output on the task sheet, as well as the glossary, to create the
model structure. (I realised part of the way through the stage 2 that creating a whole model for coordinates was 
overkill, as I'm a little unfamiliar with GeoDjango. This became more understood to me approaching the coordinates 
proximity ordering. I'd have likely saved myself some trouble had I made them a `PointField` on `Location`!)

I then created a management command to import and process the data, looking through the test data to see how to extract
relevant fields and create model instances. The script is absent of any error handling, primarily because I didn't want
to spend too much time trying to account for model errors, but normally we'd want to ensure it was robust against poor
data shapes! (Pydantic is great for validating errors and reporting them back effectively.) There's some basic logging
in there to help demonstrate the task is actually running, too. It's probably not the most performant it could be, as
we're making lots of DB calls (something ideally mitigated by bulk creation), but as there are foreign keys, this could
become unwieldy. We'd need to ensure that any foreign key instances to a location were saved before the bulk create (as
well as update the unsaved location references to the now-saved keys). It felt like a problem that could take up a lot
of the time, so I decided to document it here instead.

I wrote some generic views for the `location` and `locations` endpoints. I would have probably gone with a `ViewSet` had
it not been explicitly requested that we have the specific endpoint names, as there's a bit of duplication in there, but
I figured keeping exact to the outlined requirements was the most important factor. The endpoints do require
authentication, of course (an assumption).

I then wrote the necessary serializers to achieve the expected response data, which was pretty straightforward. I then
wrote the tests for everything (they're not the prettiest tests ever, but I didn't want to spend too much time making
them pretty, to save more for the good stuff in the next section!) The test for the management command would want a
proper fixture and more thorough checking of model instances, but (again) in the interest of time, I opted for a simpler
test.

Did some manual testing with the provided data, adding it to the docker containing, running the command and then calling
the views with cURL (I removed the view permissions for ease for that bit).

### Getting serious
For this section I knew that the ordering by proximity to a set of coordinates would be the most timely part, so I set
it aside to quickly make the Admin. I did notice that the page was displaying Countries as "Countrys", so I updated the
model's verbose plural name.

I added the `django_filters` package so that I could create a quick filter set for the locations view. The country and
operator reference were easy enough, as they just needed to point to the reference field, but the ordering by created/
updated at required updating the model. I chose to make an abstract model, as this is likely something we'd want to
re-use.

By this point, I was running low on time, so when I was doing some research on how to best go about the ordering by
proximity to a given set oif coordinates, I realised that PostGIS was already the Docker image being used for the DB on 
the `docker-compose.yml`, and so I revised my initial approach to coordinates. I decided these would have been better
served as a `PointField`, and then we annotate the queryset with the calculated distance from the given point, and then 
order by that value. The migration to a point field prove tricky, however, and I unfortunately ran out of time before I
could get it to work, but I would otherwise have researched if there was anything I was missing in my conversion, and 
read the GeoDjango docs for more background on the library.

I wrote a test anyway to demonstrate the expected output, which is currently skipped as the functionality is incomplete.
I feel like with an extra hour, I'd be there!

### Advanced
While I didn't ge to this section, I did give it a read at the beginning and have thoughts about how I might approach
it after attempting the other sections.

I'd obviously need start by adding the new fields `access_type` and `is_integrated` to the `Location` model.

I'd then create a new management command to process the supplementing data, attempting to retrieve an existing location
via the matching of the address or operator reference. We may need to fuzzy match the address, if we wanted to account
for formatting differences. For the coordinates, we can follow the same pattern as the idea in section 2, where we
create a `Point` from the coordinates and attempt to retrieve any locations in the db within 10m, using `Distance`.

If no match is found, we'd need to create fresh model instances, with `is_integrated=False`. 

(We might also want to check if the supplementing data contains extra EVSEs or connectors and update accordingly?)
