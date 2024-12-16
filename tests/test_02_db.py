import pytest
from sqlalchemy.sql.sqltypes import String, Integer
from sqlalchemy.ext.declarative import DeclarativeMeta
from dotenv import load_dotenv
from datetime import date
load_dotenv()

@pytest.fixture
def client():
    from app import app
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["DEBUG"] = False

    with app.test_client() as client:
        with app.app_context():
            from app.models import db
            db.drop_all()
            db.create_all()
        yield client


def test_configuration_has_database_setting():
    from app.config import Configuration
    for component in ["sqlite:///", "dev.db"]:
        assert component in Configuration.SQLALCHEMY_DATABASE_URI


def test_sqlalchemy_database_uri_configured_properly():
    from app import app
    from app.config import Configuration
    assert app.config.get("SQLALCHEMY_DATABASE_URI", "") == Configuration.SQLALCHEMY_DATABASE_URI


def test_model_class_has_proper_table_name():
    from app.models import Instrument
    assert Instrument.__tablename__ == "instruments"


@pytest.mark.parametrize("name,type,pk,nullable", [
    ("id", "INTEGER", True, False),
    ("date_bought", "DATE", False, False),
    ("nickname", "VARCHAR(50)", False, False),
    ("year", "INTEGER", False, True),
    ("maker", "VARCHAR(50)", False, True),
    ("type", "VARCHAR(50)", False, False),
    ("used", "BOOLEAN", False, False),
])
def test_instrument_has_good_mappings(name, type, pk, nullable):
    from app.models import Instrument
    attr = getattr(Instrument, name)
    assert name == attr.__dict__.get("key", "")
    assert pk == attr.primary_key
    assert type == str(attr.type)
    assert nullable == attr.nullable


@pytest.mark.parametrize("date_bought,maker,type", [
    ('2018-09-08', "Gibson", "String"),
    ('2018-09-08', None, "String"),
])
def test_post_of_good_data(client, date_bought, maker, type):
    rr = client.post(
        '/new_instrument',
        data={'date_bought': date_bought,
              'nickname': 'My Instrument',
              'type': type,
              'used': "False"},
        follow_redirects=True
    )
    content = rr.data.decode("utf-8")
    assert "My Instrument" in content


@pytest.mark.parametrize("date_bought,maker,type", [
    ('2018/09/08', "Gibson", "String"),
    ('2018-09-08', "", "guitar")
])
def test_post_of_bad_data(client, date_bought, maker, type):
    rr = client.post(
        '/new_instrument',
        data={'date_bought': date_bought,
              'nickname': 'nickname',
              'type': type,
              'used': "False"},
        follow_redirects=True
    )
    content = rr.data.decode("utf-8")
    assert "Bad Data" in content


def test_simple_form_data_retrieval(client):
    from app import app
    with app.app_context():
        from app.models import db, Instrument
        db.session.add(Instrument(date_bought=date(1953, 12, 13),
                                  nickname="Mary",
                                  year="1953",
                                  maker="Gibson",
                                  type="String",
                                  used=False))
        db.session.add(Instrument(date_bought=date(1987, 5, 10),
                                  nickname="Blue",
                                  year="1983",
                                  maker="Fernandes",
                                  type="String",
                                  used=True))
        
        db.session.commit()

    r = client.get("/instrument_data")
    content = r.data.decode("utf-8")
    assert "Mary" in content
    assert "Blue" not in content
    assert "1953" in content
    assert "1983" not in content
    assert "Gibson" in content
    assert "Fernandes" not in content
