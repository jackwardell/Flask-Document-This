import pytest
# from flask_api_docs.custom_flask import Flask
from flask import Flask
from flask import jsonify
from flask import request

from flask_document_this.document_this import DocumentThis

document_this = DocumentThis()


class UserAPI:
    route = "/user/<username>"
    methods = {"GET", "POST", "DELETE", "PUT"}
    endpoints = {"get_user", "post_user", "delete_user", "put_user"}


@pytest.fixture
def app():
    app = Flask("Test API")
    document_this.init_app(app)

    @app.route("/ping")
    def ping():
        return "pong"

    return app


default_docs = {
    "info": {"title": "Test API", "version": "1.0.0"},
    "openapi": "3.0.3",
    "paths": {
        "/user/<username>": {
            "delete": {
                "deprecated": False,
                "responses": {
                    "200": {"description": "Request fulfilled, document follows"}
                },
                "summary": "user",
                "tags": ["user"],
            },
            "get": {
                "deprecated": False,
                "responses": {
                    "200": {"description": "Request fulfilled, document follows"}
                },
                "summary": "user",
                "tags": ["user"],
            },
            "post": {
                "deprecated": False,
                "responses": {
                    "200": {"description": "Request fulfilled, document follows"}
                },
                "summary": "user",
                "tags": ["user"],
            },
            "put": {
                "deprecated": False,
                "responses": {
                    "200": {"description": "Request fulfilled, document follows"}
                },
                "summary": "user",
                "tags": ["user"],
            },
            "summary": "user",
        }
    },
    "servers": [{"url": "localhost:5000"}],
    "tags": [{"name": "user"}],
}


def test_app_works(app):
    with app.test_client() as client:
        r = client.get("/docs")
        assert r.status_code == 200

        r = client.get("/docs.json")
        assert r.status_code == 200


def test_app_with_all_methods_decorator(app):
    api = UserAPI()

    @app.route(api.route, methods=api.methods)
    @document_this
    def user(username):
        return jsonify(url=request.path, method=request.method, username=username)

    with app.test_client() as client:
        for method in api.methods:
            assert getattr(client, method.lower())("/user/hello").status_code == 200

        r = client.get("/docs")
        assert r.status_code == 200

        docs = client.get("/docs.json").json
        assert default_docs == docs


def test_app_with_separate_methods_decorator(app):
    api = UserAPI()

    @app.route(api.route, methods=["GET"])
    @document_this
    def get_user(username):
        return jsonify(url=request.path, method=request.method, username=username)

    @app.route(api.route, methods=["POST"])
    @document_this
    def post_user(username):
        return jsonify(url=request.path, method=request.method, username=username)

    @app.route(api.route, methods=["DELETE"])
    @document_this
    def delete_user(username):
        return jsonify(url=request.path, method=request.method, username=username)

    @app.route(api.route, methods=["PUT"])
    @document_this
    def put_user(username):
        return jsonify(url=request.path, method=request.method, username=username)

    with app.test_client() as client:
        for method in api.methods:
            assert getattr(client, method.lower())("/user/hello").status_code == 200

        docs = client.get("/docs.json").json
        assert default_docs == docs

# def create_app():
#     app = Flask(__name__)
#     document_this.init_app(app)
#
#     @document_this
#     @app.route("/pet", methods=["PUT", "POST"])
#     def pet():
#         return jsonify(route="pet")
#
#     @app.route("/pet/<pet_id>", methods=["GET", "POST", "DELETE"])
#     def pet_by_id(pet_id):
#         return jsonify(route="pet", id=pet_id)
#
#     @document_this
#     @app.post("/pet/<pet_id>/upload-image")
#     def pet_upload_image(pet_id):
#         return jsonify(route="pet", id=pet_id, endpoint="upload-image")
#
#     @app.get_and_post("/hello")
#     def hello():
#         return jsonify(hello='hello')
#
#     @app.route("/user", methods=["POST"])
#     def create_user():
#         return jsonify(route='user')
#
#     @app.route('/user/login', methods=["GET"])
#     def login_user():
#         return jsonify(route='login')
#
#     @app.route('/user/logout', methods=["GET"])
#     def logout_user():
#         return jsonify(route='logout')
#
#     @app.route('/user/<username>', methods=['GET'])
#     def get_user(username):
#         return jsonify(route='get user')
#
#     @app.route('/user/<username>', methods=['PUT'])
#     def update_user(username):
#         return jsonify(route='update user')
#
#     @app.route('/user/<username>', methods=["DELETE"])
#     def delete_user(username):
#         return jsonify(route='delete user')
#
#     return app
#
#
# app = create_app()
#
# app.run(port=5012)
#
# config = Configuration()
#
# factory = Factory(config=config)
