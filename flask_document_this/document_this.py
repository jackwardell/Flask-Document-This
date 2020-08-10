import functools
from typing import Iterable
from collections import defaultdict
import attr
from flask import jsonify
from flask import url_for
from jinja2 import Template

from flask_document_this.factory import Factory

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


@attr.s(frozen=True, slots=True)
class Method:
    method = attr.ib(converter=lambda x: x.upper())

    @method.validator
    def validate_method(self, attribute, value):
        if value not in HTTP_METHODS:
            raise ValueError(f"{attribute} must be in {HTTP_METHODS} not {value}")

    def __str__(self):
        return str(self.method)


@attr.s(frozen=True, slots=True)
class URLRoute:
    url = attr.ib()

    @property
    def group(self):
        return self.url.split("/")[1].split(".")[0]


def make_method_operation(method, route, endpoint):
    # todo fix this
    return MethodOperation(method, route, endpoint)


@attr.s
class MethodOperation:
    method = attr.ib(converter=Method)
    url_route = attr.ib(converter=URLRoute)
    summary = attr.ib(default=None)

    def to_operation(self):
        factory = Factory()
        response = factory.make_response()
        responses = factory.make_responses([response])
        operation = factory.make_operation(
            responses, [self.url_route.group], summary=self.summary
        )
        return operation


class Routes(Iterable):
    def __init__(self):
        self.routes = defaultdict(list)

    def add(self, route):
        return self.routes[route.url].append(route)

    def __iter__(self):
        return iter(self.routes)

    def __setitem__(self, route):
        return self.routes[route.url].append(route)

    def to_list(self):
        return [route.to_json() for route in self.routes]

    def to_paths(self):
        factory = Factory()
        return factory.make_paths([route.to_path() for route in self.routes])

    def to_tags(self):
        tags = []
        factory = Factory()

        for route in self.routes:
            if route.group not in tags:
                tags.append(route.group)
        return factory.make_tags(tags)


@attr.s
class DocumentStore:
    store = attr.ib(factory=dict)

    def set(self, name, value):
        self.store[name] = value

    def get(self, name):
        return self.store.get(name)


@attr.s
class Document:
    pass


class DocumentThis:
    document_routes = Routes()

    # documented_endpoints = DocumentStore()

    def __init__(self, app=None, name=None, api_version="1.0.0"):
        self.name = name
        self.api_version = api_version
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault("DOCUMENT_RULE", "/docs")
        app.config.setdefault("DOCUMENT_ENDPOINT", "docs")

        app.config.setdefault("")
        app.document_this = self
        self.add_docs_route(app)
        self.make_routes(app)

        if self.name is None:
            self.name = app.name


    def add_docs_route(self, app):
        rule = app.config.get("DOCUMENT_RULE")
        endpoint = app.config.get("DOCUMENT_ENDPOINT")

        @app.route(rule, endpoint=endpoint)
        def docs_page():
            """docs page"""
            # routes = make_routes_from_app(app)
            template = Template(html)
            return template.render(docs_json=url_for(endpoint + "_json"))

        @app.route(rule + ".json", endpoint=endpoint + "_json")
        def docs_json():
            """docs json"""
            # routes = make_routes_from_app(app)
            from flask import current_app

            routes = self.make_routes(current_app)
            factory = Factory()

            info = factory.make_info(self.name, self.api_version)
            paths = routes.to_paths()
            server_url = current_app.config.get("SERVER_NAME") or "localhost:5000"
            servers = [factory.make_server(server_url)]
            tags = routes.to_tags()
            api = factory.make_open_api(paths, info, servers, tags=tags).to_dict()
            return jsonify(api)

        @app.route("/embed")
        def embed():
            from IPython import embed

            embed()
            return "hello world"

    def with_model(self, model):
        def decorator(func):
            document_this(func)

            func.__model__ = model

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    # def with_kwargs(self, **kwargs):
    #     def decorator(func):
    #         document_this(func)
    #
    #         @functools.wraps(func)
    #         def wrapper(*args, **kwargs):
    #             return func(*args, **kwargs)
    #
    #         return wrapper
    #
    #     return decorator

    def __call__(self, func):
        return document_this(func)
        # self.documented_endpoints.set()

    @staticmethod
    def make_routes(app):
        routes = Routes()
        rules = defaultdict(list)

        for rule in app.url_map.iter_rules():
            view_func = app.view_functions[rule.endpoint]
            # import IPython; IPython.embed()
            if is_documented(view_func):
                for method in rule.methods:
                    if method not in ("OPTIONS", "HEAD"):
                        # rule_map = RuleMap(rule.rule, rule, view_func, method)
                        # rule_maps.append(rule_map)
                        rules[rule.url].append(
                            make_method_operation(method, rule.rule, rule.endpoint)
                        )
        for rule, data in rules.items():
            route = make_route(rule, rules[rule.url], view_func)
            routes.add(route)

        # if is_documented(view_func):
        #     operations = []
        #     for method in rule.methods:
        #         if method not in ("OPTIONS", "HEAD"):
        #             method_operation = make_method_operation(
        #                 method, rule.rule, rule.endpoint
        #             )
        #             operations.append(method_operation)
        #
        #     route = make_route(rule, operations, view_func)
        #     routes.add(route)
        return routes

    def make_open_api(self):
        factory = Factory()
        info = factory.make_info(self.name, self.api_version)
        paths = self.document_routes.to_paths()
        return factory.make_open_api(paths, info)

    def make_open_api_dict(self):
        return self.make_open_api().to_dict()

    def make_open_api_dict2(self):
        return


@attr.s
class RouteX:
    url = attr.ib()
    ops = attr.ib()
    ...
    "fill in below more features"
    "route needs to encapsulate all operations"


@attr.s
class RuleMap:
    url = attr.ib()
    rule = attr.ib()
    func = attr.ib()
    method = attr.ib()


# def make_routes_from_app(flask_app):
#     routes = Routes()
#     for rule in flask_app.url_map.iter_rules():
#         view_func = flask_app.view_functions[rule.endpoint]
#         for method in rule.methods:
#             if method not in ("OPTIONS", "HEAD"):
#                 route = Route(rule.rule, method, rule.endpoint, view_func.__doc__)
#                 routes.add(route)
#             else:
#                 pass
#     return routes


def make_route(rule, operations, view_func):
    return Route(
        rule.rule,
        operations,
        rule.endpoint,
        rule.rule.split("/")[1].split(".")[0],
        view_func.__doc__,
    )


class BaseModel:
    @property
    def entity(self):
        raise NotImplementedError()

    @property
    def fields(self):
        raise NotImplementedError()

    def find(self, **kwargs):
        raise NotImplementedError()


# class SqlAlchemyModel(BaseModel):
#
#     def find(self, **kwargs):
#         return

# responses = {}


class Route:
    def __init__(self, url, operations, endpoint, group, doc):
        self.url = url
        self.operations = operations
        self.doc = doc
        self.endpoint = endpoint
        self.group = group

    def to_json(self):
        # embed()
        rv = {
            # todo parse out < to { and > to }
            "url": self.url,
            "operations": self.operations,
            "endpoint:": self.endpoint,
            "doc": self.doc,
        }
        return rv

    def to_path(self):
        factory = Factory()
        # response = factory.make_response()
        # responses = factory.make_responses([response])
        # operation = factory.make_operation(
        #     responses, [self.group], summary=self.endpoint.replace("_", " ")
        # )

        ops = {str(i.method): i.to_operation() for i in self.operations}

        kwargs = {
            "ref": self.url[1:],
            "summary": self.endpoint.replace("_", " "),
            "description": self.doc,
        }

        kwargs.update(ops)
        path = factory.make_path(**kwargs)
        return path


class _Documenter:
    attr_name = "__document_this__"

    @classmethod
    def document_this(cls, func):
        setattr(func, cls.attr_name, True)
        return func

    @classmethod
    def is_documented(cls, func):
        return hasattr(func, cls.attr_name)

    @classmethod
    def find_document(cls, func):
        return getattr(func, cls.attr_name) if cls.is_documented(func) else None


document_this = _Documenter.document_this
is_documented = _Documenter.is_documented
find_document = _Documenter.find_document

html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <script src="//unpkg.com/swagger-ui-dist@3/swagger-ui-standalone-preset.js"></script>
    <!-- <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.22.1/swagger-ui-standalone-preset.js"></script> -->
    <script src="//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js"></script>
    <!-- <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.22.1/swagger-ui-bundle.js"></script> -->
    <link rel="stylesheet" href="//unpkg.com/swagger-ui-dist@3/swagger-ui.css"/>
    <!-- <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.22.1/swagger-ui.css" /> -->
    <title>Swagger</title>
</head>
<body>
<div id="swagger-ui"></div>
<script>
    window.onload = function () {
        SwaggerUIBundle({
            url: "{{ docs_json }}",
            dom_id: '#swagger-ui',
            presets: [
                SwaggerUIBundle.presets.apis,
                SwaggerUIStandalonePreset
            ],
            layout: "StandaloneLayout"
        })
    }
</script>
</body>
</html>
"""
