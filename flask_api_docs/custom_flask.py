from flask import Flask as _Flask
from functools import partial

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


class Flask(_Flask):
    def get(self, rule, **options):
        return self.route(rule, methods=["GET"], **options)

    def head(self, rule, **options):
        return self.route(rule, methods=["HEAD"], **options)

    def post(self, rule, **options):
        return self.route(rule, methods=["POST"], **options)

    def put(self, rule, **options):
        return self.route(rule, methods=["PUT"], **options)

    def delete(self, rule, **options):
        return self.route(rule, methods=["DELETE"], **options)

    def connect(self, rule, **options):
        return self.route(rule, methods=["CONNECT"], **options)

    def options(self, rule, **options):
        return self.route(rule, methods=["OPTIONS"], **options)

    def trace(self, rule, **options):
        return self.route(rule, methods=["TRACE"], **options)

    def patch(self, rule, **options):
        return self.route(rule, methods=["PATCH"], **options)

    def __getattr__(self, item):
        potential_methods = [i for i in item.split("_") if i not in ("and", "or")]
        if len(potential_methods) < 2:
            raise AttributeError(f"{item} not found")
        else:
            methods = set(m.upper() for m in potential_methods)
            if methods.issubset(HTTP_METHODS):
                return partial(self.route, methods=methods)
            else:
                raise AttributeError(f"{potential_methods} are not all http methods")
