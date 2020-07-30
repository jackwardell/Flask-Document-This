import attr

from flask_api_docs.specification import *
from flask_api_docs.specification import Info
from flask_api_docs.specification import OpenAPI
from flask_api_docs.specification import Paths
from flask_api_docs.specification import Server

DEFAULT_OPEN_API_SPECIFICATION_VERSION = "3.0.3"
DEFAULT_SERVER = Server("/")
DEFAULT_TITLE = "My first API"


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


def make_default_open_api():
    open_api = "3.0.1"
    info = make_info()


def make_open_api(open_api: str, info: Info, paths: Paths):
    OpenAPI()


def make_server():
    return Server()


@attr.s
class Configuration:
    title = attr.ib(default="My first API")
    version = attr.ib(default="1.0.0")
    terms_of_service = attr.ib(default=None)

    def get(self, item, default=None):
        return getattr(self, item, default)

    def __getitem__(self, item):
        return getattr(self, item)


@attr.s
class Factory:
    config = attr.ib(factory=dict)

    def make_open_api(self):
        open_api = DEFAULT_OPEN_API_SPECIFICATION_VERSION
        info = self.make_info()
        servers = [DEFAULT_SERVER]
        paths = self.make_paths()
        return OpenAPI(open_api, info, paths, servers)

    def make_info(self):
        title = self.config.get('title', 'my first api')
        version = self.config.get('version', '1.0.0')
        return Info(title, version)

    def make_paths(self):
        # from IPython import embed; embed()
        return Paths([self.make_path('hello'), self.make_path('goodbye')])

    def make_path(self, x):
        return Path(ref=x)


f = Factory()

print(f.make_open_api().to_dict())
