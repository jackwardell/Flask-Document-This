from flask import jsonify

from flask_document_this.document_this import DocumentThis
from flask_document_this.factory import Configuration
from flask_document_this.factory import Factory
from flask_document_this.custom_flask import Flask

document_this = DocumentThis()


def create_app():
    app = Flask(__name__)
    document_this.init_app(app)

    @document_this
    @app.route("/pet", methods=["PUT", "POST"])
    def pet():
        return jsonify(route="pet")

    @app.route("/pet/<pet_id>", methods=["GET", "POST", "DELETE"])
    def pet_by_id(pet_id):
        return jsonify(route="pet", id=pet_id)

    @document_this
    @app.post("/pet/<pet_id>/upload-image")
    def pet_upload_image(pet_id):
        return jsonify(route="pet", id=pet_id, endpoint="upload-image")

    @app.get_and_post("/hello")
    def hello():
        return jsonify(hello='hello')

    @app.route("/user", methods=["POST"])
    def create_user():
        return jsonify(route='user')

    @app.route('/user/login', methods=["GET"])
    def login_user():
        return jsonify(route='login')

    @app.route('/user/logout', methods=["GET"])
    def logout_user():
        return jsonify(route='logout')

    @app.route('/user/<username>', methods=['GET'])
    def get_user(username):
        return jsonify(route='get user')

    @app.route('/user/<username>', methods=['PUT'])
    def update_user(username):
        return jsonify(route='update user')

    @app.route('/user/<username>', methods=["DELETE"])
    def delete_user(username):
        return jsonify(route='delete user')

    return app


app = create_app()

app.run(port=5012)

config = Configuration()

factory = Factory(config=config)
