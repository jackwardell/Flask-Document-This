from collections.abc import Iterable
from functools import wraps

from IPython import embed
from flask import jsonify


class Document:
    document_routes = []

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault("DOCUMENT_RULE", "/docs")
        app.config.setdefault("DOCUMENT_ENDPOINT", "docs")

        app.config.setdefault("")
        app.document = self
        self.add_docs_route(app)

    def add_docs_route(self, app):
        rule = app.config.get("DOCUMENT_RULE")
        endpoint = app.config.get("DOCUMENT_ENDPOINT")

        @app.route(rule, endpoint=endpoint)
        def docs_page():
            """hello"""
            routes = make_routes_from_app(app)
            # embed()
            return jsonify(routes.to_list())

    def this(self, func):
        # embed()
        return func


# class RouteMap(Iterable):
#     def __init__(self, app):
#         routes = make_routes_from_app(app)
#
#     def __iter__(self):
#         return self.url_map.iter_rules()


def make_routes_from_app(flask_app):
    routes = Routes()
    for rule in flask_app.url_map.iter_rules():
        view_func = flask_app.view_functions[rule.endpoint]
        for method in rule.methods:
            route = Route(rule.rule, method, view_func.__doc__)
            routes.add(route)
    return routes


class Routes(Iterable):
    def __init__(self, routes=None):
        self.routes = routes or []

    def add(self, route):
        self.routes.append(route)

    def __iter__(self):
        return iter(self.routes)

    def to_list(self):
        return [route.to_json() for route in self.routes]


class Route:

    def __init__(self, url, method, doc):
        self.url = url
        self.method = method
        self.doc = doc

    def to_json(self):
        # embed()
        return {'url': self.url, 'method': self.method, 'doc': self.doc}


def document_this(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


# import flask
#
# app = flask.Flask("s")
# document = Document(app)
#
#
# @document.this
# @app.route('/h')
# def h():
#     return 'jh'
#
#
# app.run(host='localhost', port=5001, debug=True)
#
