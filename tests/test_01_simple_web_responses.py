import pytest
from wtforms import IntegerField, StringField, SubmitField, TextAreaField, \
                    DateField, SelectField, BooleanField
from flask_wtf import FlaskForm
from dotenv import load_dotenv
load_dotenv()

@pytest.fixture
def client():
    from app import app
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["DEBUG"] = False

    with app.test_client() as client:
        yield client


def test_main_page_has_message(client):
    r = client.get("/")
    assert b"<h1>Python Flask Assessment</h1>" in r.data
    assert "Content-Type" in r.headers
    assert "text/html" in r.headers.get("Content-Type", "")


@pytest.mark.parametrize("field", [
    '<input id="date_bought" name="date_bought" required',
    '<input id="nickname" name="nickname" required',
    '<input id="year" name="year"',
    '<input id="maker" name="maker"',
    '<select id="type" name="type"',
    '<input id="used" name="used"',
    '<input id="submit" name="submit" type="submit" value="Submit">',
])
def test_simple_form_page(client, field):
    rr = client.get("/new_instrument")
    content = rr.data.decode("utf-8")

    assert '<form method="post" action="/new_instrument">' in content
    assert field in content


@pytest.mark.parametrize("name,type,label", [
    ("date_bought", DateField, "Date Bought"),
    ("nickname", StringField, "Nickname"),
    ("year", IntegerField, "Year"),
    ("maker", StringField, "Maker"),
    ("type", SelectField, "Type"),
    ("used", BooleanField, "Used"),
    ("submit", SubmitField, "Submit"),
])
def test_simple_form_class(name, type, label):
    from app.forms import NewInstrument
    assert FlaskForm in NewInstrument.__bases__
    attr = getattr(NewInstrument, name)
    assert attr.field_class == type
    assert label in attr.args
