from flask_document_this.specification import *
from flask_document_this.specification import Info
from flask_document_this.specification import OpenAPI
from flask_document_this.specification import Operation
from flask_document_this.specification import Paths
from flask_document_this.specification import Response
from flask_document_this.specification import Responses
from flask_document_this.specification import Server
from flask_document_this.specification import Tag

DEFAULT_OPEN_API_SPECIFICATION_VERSION = "3.0.3"
DEFAULT_SERVER = Server("/")
DEFAULT_TITLE = "My first API"

HTTP_METHODS = {
    "GET",
    "HEAD",
    "POST",
    "PUT",
    "DELETE",
    "CONNECT",
    "OPTIONS",
    "TRACE",
    "PATCH",
    "OPTIONS",
}


# def make_config(app):
#     title = app.config.get("API_TITLE")
#     version = app.config.get("API_VERSION")
#
#     return Configuration(title=app.name)


def make_info(
        title: str,
        version: str,
        description=None,
        terms_of_service=None,
        contact=None,
        license=None,
):
    return Info(title, version)


# def make_default_open_api():
#     open_api = "3.0.1"
#     info = make_info()
#
#
# def make_open_api(open_api: str, info: Info, paths: Paths):
#     OpenAPI()
#
#
# def make_server():
#     return Server()


@attr.s
class Configuration:
    title = attr.ib(default="My first API")
    version = attr.ib(default="1.0.0")
    terms_of_service = attr.ib(default=None)

    def get(self, item, default=None):
        return getattr(self, item, default)

    def __getitem__(self, item):
        return getattr(self, item)


from http import HTTPStatus


@attr.s
class Factory:
    config = attr.ib(factory=dict)

    def make_responses(self, responses, default=None):
        # todo fix this
        return Responses(responses=responses, default=default or [])

    def make_response(self, status_code=200):
        status = HTTPStatus(status_code)
        return Response(status.description, status.value)

    def make_operation(self, responses, tags, summary):
        return Operation(responses, tags, summary)

    def make_tags(self, tags):
        return [Tag(tag) for tag in tags]

    def make_open_api(self, paths, info, servers=None, tags=None):
        open_api = DEFAULT_OPEN_API_SPECIFICATION_VERSION
        info = info
        servers = servers or [DEFAULT_SERVER]
        paths = paths
        # from IPython import embed; embed()
        return OpenAPI(open_api, info, paths, servers, tags=tags)

    def make_server(self, url):
        return Server(url)

    def make_info(self, title, version="1.0.0"):
        # title = self.config.get("title", "my first api")
        # version = self.config.get("version", "1.0.0")
        return Info(title, version)

    def make_paths(self, paths):
        # from IPython import embed; embed()
        return Paths(paths)

    def make_path(self, **kwargs):
        kwargs = {i.lower(): j for i, j in kwargs.items()}
        if 'ref' not in kwargs:
            raise ValueError("must have ref")

        if 'summary' not in kwargs:
            raise ValueError("must have summary")

        if "description" not in kwargs:
            raise ValueError("must have description")

        # passed_methods = set([i.upper() for i in kwargs.keys()])
        #
        # for method in passed_methods & HTTP_METHODS:

        return Path(**kwargs)

#
# f = Factory()
#
# print(f.make_open_api().to_dict())
