import pytest
from custom_flask import Flask

from flask_api_docs.document_this import document_this
from flask_api_docs.document_this import DocumentThis


@pytest.fixture
def app():
    return Flask("test_app")


@pytest.fixture
def documented_app(app):
    document = DocumentThis()
    document.init_app(app)
    return app


@pytest.fixture
def documented_test_client(documented_app):
    with documented_app.test_client() as client:
        yield client


def test_document_no_app():
    document = DocumentThis()
    assert document


def test_document_with_app(app):
    assert "DOCUMENT_RULE" not in app.config
    assert "DOCUMENT_ENDPOINT" not in app.config

    document = DocumentThis(app)
    assert document
    assert app.config["DOCUMENT_RULE"] == "/docs"
    assert app.config["DOCUMENT_ENDPOINT"] == "docs"


def test_document_with_app_factory():
    document = DocumentThis()

    def app_factory():
        flask_app = Flask("app_factory")
        document.init_app(flask_app)
        return flask_app

    app = app_factory()
    assert app.config["DOCUMENT_RULE"] == "/docs"
    assert app.config["DOCUMENT_ENDPOINT"] == "docs"


def test_docs_page_exists(documented_app):
    rules = [i.rule for i in documented_app.url_map.iter_rules()]
    assert "/docs" in rules
    assert documented_app.config.get("DOCUMENT_RULE") in rules


def test_docs_page_works(documented_test_client):
    resp = documented_test_client.get("/docs")
    assert resp.status_code == 200
    assert "hello world" in resp.data.decode()


def test_document_this(documented_app):
    @document_this
    @documented_app.route('/ping')
    def ping():
        return "pong"
