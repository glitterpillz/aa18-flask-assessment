# Python 2a Assessment - Flask

Welcome to the Python Flask Assessment!

In this assessment, you will create a simple, data-driven web application using
Python. The tests are provided for you in this project; however, there is an
incomplete Pipfile because part of this assessment is for you to initialize and
use your own virtual environment using Pipenv.

* __Total Possible Points:__ 30 points  
* __Points Required to Pass:__ 24 points

You will have **3 hours** to complete the assessment.

## Resources

For this assessment, you are allowed to use the following resources:

* [MDN]
* A whiteboard or paper to work out problems/code, but they must be within
  camera range
* VS Code or a console for testing and experimentation
* Node
* Postman (when useful)
* Official documentation, including:
  * [Python]
  * [Flask]
  * [WTForms]
  * [FlaskWTF]
  * [Jinja]
  * [Flask-migrate]
  * [FlaskSQLAlchemy]
  * [SQLAlchemy]
  * [Alembic-documentation]

You are **NOT** allowed to refer to any other resources, including--but not
limited to--other websites (e.g., a/A curriculum on Canvas, StackOverflow),
communication apps (e.g., Slack, Discord), search engines, notes, or any of your
previously written code.

## Getting started

Clone the assessment at the bottom of this page.

Your application should use a SQLite3 database.

Use Pipenv to install the following dependencies.

* pytest
* pycodestyle
* pylint
* rope
* flask
* flask-sqlalchemy
* alembic
* flask-migrate
* python-dotenv
* sqlalchemy
* wtforms
* flask-wtf

Once you have those installed, activate your virtual environment.

The tests will expect you to store your application's code in an __app/__
directory. Inside the __app/__ directory, you will need to

* Edit the __\_\_init\_\_.py__ file which will contain your Flask app
  declaration
* Edit the __forms.py__ file which will contain your form classes
* Edit the __models.py__ file which will contain your Flask-SQLAlchemy model
  classes.
* Edit the __config.py__ file which will contain your configuration object

**NOTE 1:** The autograder will have a `DATABASE_URL` environment variable set
with the address of the sqlite database.

**NOTE 2:** If you are going to view this application in the browser while you
develop it, you will need to set a `SECRET_KEY` in your configuration. The unit
tests do not require it to be set. There is a reminder, later, to add it when
you'll need it.

## The requirements

For each of the following routes, you need to implement the requirements. These
requirements are what the tests test.

Test your application by running the command `pytest` from the root directory.

### App location

In the __app/\_\_init\_\_.py__ file, create your Flask application. You must
name the variable that holds the Flask application `app`.

You can define the routes wherever you'd like: in their own Blueprints using the
files in the __routes__ folder, or in the __app/\_\_init\_\_.py__ file.

Think of what you will need to import into the __\_\_init\_\_.py__ file in the
root of the project directory.

### GET "/"

The response from this HTTP request must be of type "text/html" (Flask sets this
for you when you render a template) and contain the following HTML:

```html
<h1>Python Flask Assessment</h1>
```

### GET "/new_instrument"

You must create a form class using Flask-WTF and WTForms. You must define this
in the `app.forms` module. The form class must be named `NewInstrument`. It must
define a form with the following specifications.

| Field name | Label        | Data type to collect   | Validators    |
|------------|------------- |------------------------|---------------|
| date_bought| "Date Bought"| date                   | data required |
| nickname   | "Nickname"   | string                 | data required |
| year       | "Year"       | integer                |               |
| maker      | "Maker"      | string                 |               |
| type       | "Type"       | string from dropdown   |               |
| used       | "Used"       | boolean                | data required |
| submit     | "Submit"     | n/a                    |               |

**NOTE:** The `type` field must display a drop-down menu with the following
options: _Other, String, Woodwind, Brass, Percussion_.

Create a route to handle `GET /new_instrument`. In it use the form class you
just defined and render a template containing the form HTML.

The response from this HTTP request must be of type "text/html" (Flask sets this
for you when you render a template) and contain the form fields described above.
The method of the form should be "post" and "/new_instrument". While PEP8 does
not have an opinion on single quotes vs. double quotes, the unit test does!

### **The form tag should look exactly like this.**

```html
<form method="post" action="/new_instrument">
```

**NOTE:** If you are going to view this in the browser, then you need to do
things:

* Don't forget to put the `{{ form.csrf_token }}` value in your form. (The
  `form` variable, there, is whatever you name the form parameter for the
  template.)
* Go ahead and create a class named `Configuration` in `app.config`. Add a
  `SECRET_KEY` value to it. Get that configuration into your application by
  following the instructions in the next section.

### POST "/new_instrument"

In the `app.config` module, create a class named `Configuration`. In there,
create an attribute named `SQLALCHEMY_DATABASE_URI` and set it to the value of
`'sqlite:///dev.db'`.

Import your environment variables into app.config.py (We trust that you know how
to use `os.environ.get`)

Notes:

* If you are going to view this in the browser, add a `SECRET_KEY` attribute to
  the `Configuration` object, as well, and set it to anything.
* SQLAlchemy will issue a warnings about `SQLALCHEMY_TRACK_MODIFICATIONS`.
  These will not effect your tests passing, and can be ignored.  Alternatively
  you may set it's value to False in your configuration object to address the
  warnings.

Import the `Configuration` class into the __app/\_\_init\_\_.py__ file and use
it to configure your Flask application.

Create a mapping class (model) in the `app.models` module named `Instrument`. It
must use the table name "instruments". It must have the following mappings on
it.

Remember that you will need to construct a `db` object by calling the
`SQLAlchemy` constructor.  In order to avoid circular dependencies (caused by
importing from `app`) import `db` into your __app/\_\_init\_\_.py__ and call
`init_app` on it.

| Column name | Data type     | Constraints |
|-------------|---------------|-------------|
| id          | INTEGER       | Primary key |
| date_bought | DATE          | not null    |
| nickname    | VARCHAR(50)   | not null    |
| year        | INTEGER       |             |
| maker       | VARCHAR(50)   |             |
| type        | VARCHAR(50)   | not null    |
| used        | BOOL          | not null    |

Create a migration for this and upgrade your database.

* Create a *separate* route to handle `POST /new_instrument`.
* It should take the data from the posted form page (date_bought, nickname,
  etc.) and use the `Instrument` validate it
* If the form validates, it should
  * use the `Instrument` to insert it into the database using the `Instrument`
  * redirect to "/instrument_data".
* If the form does not validate, it should show a message that reads "Bad Data"
  (the content type can be anything, including plain text).

### GET "/instrument_data"

Create a route to handle `GET /instrument_data`. In that route, have it query
all of the records from using the `Instrument` for where the nickname begins
with "M". Loop over those records in your view and render them using the
following template.

```html
<-- Your for loop, here -->
<div>{{ instrument.date_bought }}</div>
<div>{{ instrument.nickname }}</div>
<div>{{ instrument.year }}</div>
<div>{{ instrument.maker }}</div>
<div>{{ instrument.type }}</div>
<div>{{ instrument.used }}</div>
<div>{{ instrument.submit }}</div>
{% endfor %}
```

## The tests

The tests are grouped into two categories: simple and data-driven. The "simple"
tests do not require a database. The "data-driven" tests require you to store
data in a database by creating proper models. The model classes will be
inspected.

### The "simple" tests

These tests will check that the responses have values in the HTML and in your
`Instrument` class.

### The "database" tests

These tests will check your `Configuration` class, that those values are put
into your Flask application's `config` object, the model exist in your
`app.models` module, and that your routes handle and show data created in your
application.

## Submission

When you are ready to submit:

1. Run `pytest` in the root directory to re-run all of the tests.
  
2. Fix any syntax errors that cause the tests to crash. **If a test crashes or
   the tests fail to complete their run, you will receive a 0 for the coding
   portion of this assessment.** You can fail specs, but all the tests have to
   be able to finish running.

   **Tip:** If you run out of time to debug, just comment out any code that is
   causing your program to crash.

3. Add, commit, and push your changed files:

   ```sh
   git add .
   git commit -m "Finish the assessment (or some such descriptive message)"
   git push
   ```

   **Note:** The first time you run `git push`, git will tell you to run a more
   complete version of the command:

   ```sh
   git push --set-upstream origin <your branch>
   ```

You can run tests, `add` files, and `commit` files as often as you wish, but
only your first **two pushes** will be graded. (If for some reason you need more
than two pushes, you must plead your case to an Instructor.)

Good luck!

**Copyright App Academy. Please do not share this repo or post any parts of it
online. App Academy will take violations very seriously.**

[MDN]: https://developer.mozilla.org/en-US/
[Python]: https://docs.python.org/3/index.html
[WTForms]: https://wtforms.readthedocs.io/en/2.3.x/
[FlaskWTF]: https://flask-wtf.readthedocs.io/en/stable/
[Flask]: https://flask.palletsprojects.com/en/1.1.x/
[Flask-migrate]: https://flask-migrate.readthedocs.io/en/latest/
[FlaskSQLAlchemy]: https://flask-sqlalchemy.palletsprojects.com/en/2.x/
[SQLAlchemy]: https://docs.sqlalchemy.org/en/13/
[Alembic-documentation]: https://alembic.sqlalchemy.org/en/latest/
[Jinja]: https://jinja.palletsprojects.com/en/3.0.x/
# aa19-flask-assessment
# aa18-flask-assessment
