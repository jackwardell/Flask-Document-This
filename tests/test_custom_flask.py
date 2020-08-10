import pytest
from flask import Flask as FlaskFlask
from flask import jsonify
from flask_document_this.custom_flask import Flask as CustomFlask

HTTP_METHODS = {
    "GET",
    "HEAD",
    "POST",
    "POST",
    "PUT",
    "DELETE",
    "CONNECT",
    "OPTIONS",
    "TRACE",
    "PATCH",
}

app_name = "hello"


@pytest.fixture
def flask_app():
    return FlaskFlask(app_name)


@pytest.fixture
def custom_app():
    return CustomFlask(app_name)


def test_custom_flask_has_methods(flask_app, custom_app):
    assert len(dir(flask_app)) + len(HTTP_METHODS) + 1 == len(dir(custom_app))

    for method in HTTP_METHODS:
        assert method.lower() in dir(custom_app)

    assert "__getattr__" in dir(custom_app)

# def test_routes_match(flask_app, custom_app):
#     rv = {'hello': "world"}
#
#     def return_value(data, **kwargs):
#         data = data.update(kwargs)
#         return jsonify(data)
#
#     @flask_app.route('/hello')
#     def flask_hello():
#         return return_value(rv)
#
#     @flask_app.route('/goodbye/<name>', methods=["POST", "DELETE"])
#     def flask_goodbye(name):
#         return return_value(rv, name=name)
#
#     @custom_app.get('/hello')
#     def custom_hello():
#         return return_value(rv)
#
#     @custom_app.post('/goodbye/<name>')
#     def custom_post_goodbye(name):
#         return return_value(rv, name=name)
#
#     @custom_app.delete('/goodbye/<name>')
#     def custom_delete_goodbye(name):
#         return return_value(rv, name=name)
#
#     with flask_app.test_client() as client:
