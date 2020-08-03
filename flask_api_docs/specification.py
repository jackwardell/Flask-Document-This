import attr
import json


def ff(a, v):
    if hasattr(v, "ref"):
        return v.ref


class Serializable:
    @property
    def api_format(self):
        raise NotImplementedError()

    def to_dict(self):
        # print(self.api_format())

        # rv = {}
        # for k, v in self.api_format().items():
        #     if isinstance(v, str):
        #         rv[k] = v
        #     elif isinstance(v, list):
        #         rv[k] = [getattr(i, "to_dict", lambda: i)() for i in v]
        #     else:

        rv = {
            i: j
            if isinstance(j, str)
            else j.to_dict()
            if hasattr(j, "to_dict")
            else [getattr(k, "to_dict", lambda: k)() for k in j]
            if isinstance(j, list)
            else j
            for i, j in self.api_format().items()
            if j is not None
        }
        return rv

    def to_json(self):
        return json.dumps(self.to_dict())


def required_string(_, attribute, value):
    if not value or not isinstance(value, str):
        raise ValueError(f"{attribute} must be a str")


def required_string_as_url(_, attribute, value):
    if not value or not isinstance(value, str):
        raise ValueError(f"{attribute} must be a str")


def optional_string(_, attribute, value):
    if value and not isinstance(value, str):
        raise ValueError(f"{attribute} must be a str")


def optional_string_as_url(_, attribute, value):
    # todo
    if value and not isinstance(value, str):
        raise ValueError(f"{attribute} must be a str")


def optional_string_as_email_address(_, attribute, value):
    # todo
    if value and not isinstance(value, str):
        raise ValueError(f"{attribute} must be a str")


def required_info(_, attribute, value):
    if not value or not isinstance(value, Info):
        raise ValueError(f"{attribute} must be an 'Info' object")


def required_paths(_, attribute, value):
    if not value or not isinstance(value, Paths):
        raise ValueError(f"{attribute} must be an 'Paths' object")


def optional_list_of_servers(_, attribute, value):
    if not isinstance(value, list) or not all([isinstance(i, Server) for i in value]):
        raise ValueError(f"{attribute} must be a list of 'Server' objects")


def optional_components(_, attribute, value):
    if value and not isinstance(value, Components):
        raise ValueError(f"{attribute} must be a 'Components' object")


def optional_list_of_security_requirements(_, attribute, value):
    if value and (
            not isinstance(value, list)
            or not all([isinstance(i, SecurityRequirement) for i in value])
    ):
        raise ValueError(f"{attribute} must be a list of 'SecurityRequirement' object")


def optional_list_of_tags(_, attribute, value):
    if value and (
            not isinstance(value, list) or not all([isinstance(i, Tag) for i in value])
    ):
        raise ValueError(f"{attribute} must be a list of 'Tag' object")


def optional_external_docs(_, attribute, value):
    if value and not isinstance(value, ExternalDocumentation):
        raise ValueError(f"{attribute} must be a 'ExternalDocumentation' object")


def optional_contact(_, attribute, value):
    if value and not isinstance(value, Contact):
        raise ValueError(f"{attribute} must be a 'Contact' object")


def optional_license(_, attribute, value):
    if value and not isinstance(value, License):
        raise ValueError(f"{attribute} must be a 'License' object")


def optional_dict_of_server_variables(_, attribute, value):
    if value and not isinstance(value, ):
        raise ValueError(f"{attribute} must be a 'License' object")


@attr.s
class OpenAPI(Serializable):
    # This string MUST be the semantic version number of the OpenAPI
    # Specification version that the OpenAPI document uses. The openapi field
    # SHOULD be used by tooling specifications and clients to interpret the
    # OpenAPI document. This is not related to the API info.version string.
    open_api: str = attr.ib(validator=required_string)

    # Provides metadata about the API. The metadata MAY be used by tooling as
    # required.
    info = attr.ib(validator=required_info)

    # The available paths and operations for the API.
    paths = attr.ib(validator=required_paths)

    # An array of Server Objects, which provide connectivity information to
    # a target server. If the servers property is not provided, or is an empty
    # array, the default value would be a Server Object with a url value of /.
    servers: list = attr.ib(validator=optional_list_of_servers)

    # set default to server of '/'
    @servers.default
    def default_server(self) -> list:
        return [Server("/")]

    # An element to hold various schemas for the specification
    components: list = attr.ib(default=None, validator=optional_components)

    # A declaration of which security mechanisms can be used across the API.
    # The list of values includes alternative security requirement objects
    # that can be used. Only one of the security requirement objects need
    # to be satisfied to authorize a request. Individual operations can
    # override this definition. To make security optional, an empty security
    # requirement ({}) can be included in the array.
    security: list = attr.ib(
        default=None, validator=optional_list_of_security_requirements
    )

    # A list of tags used by the specification with additional metadata.
    # The order of the tags can be used to reflect on their order by the
    # parsing tools. Not all tags that are used by the Operation Object must
    # be declared. The tags that are not declared MAY be organized randomly
    # or based on the tools' logic. Each tag name in the list MUST be unique.
    tags: list = attr.ib(default=None, validator=optional_list_of_tags)

    # Additional external documentation.
    external_docs = attr.ib(default=None, validator=optional_external_docs)

    def api_format(self):
        rv = {
            "openapi": self.open_api,
            "info": self.info,
            "externalDocs": self.external_docs,
            "servers": self.servers,
            "tags": self.tags,
            "paths": self.paths,
            "components": self.components,
        }
        return rv


@attr.s
class Info(Serializable):
    # The title of the API.
    title: str = attr.ib(validator=required_string)

    # The version of the OpenAPI document (which is distinct from the OpenAPI
    # Specification version or the API implementation version).
    version: str = attr.ib(validator=required_string)

    # A short description of the API. CommonMark syntax MAY be used for rich
    # text representation.
    description: str = attr.ib(default=None, validator=optional_string)

    # A URL to the Terms of Service for the API. MUST be in the format of a URL.
    terms_of_service: str = attr.ib(default=None, validator=optional_string_as_url)

    # The contact information for the exposed API.
    contact = attr.ib(default=None, validator=optional_contact)

    # The license information for the exposed API.
    license = attr.ib(default=None, validator=optional_license)

    def api_format(self):
        rv = {
            "title": self.title,
            "description": self.description,
            "termsOfService": self.terms_of_service,
            "contact": self.contact,
            "license": self.license,
            "version": self.version,
        }
        return rv


@attr.s
class Contact(Serializable):
    # The identifying name of the contact person/organization.
    name: str = attr.ib(default=None, validator=optional_string)

    # The URL pointing to the contact information. MUST be in the format of a
    # URL.
    url: str = attr.ib(default=None, validator=optional_string_as_url)

    # The email address of the contact person/organization. MUST be in the
    # format of an email address.
    email: str = attr.ib(default=None, validator=optional_string_as_email_address)

    def api_format(self):
        rv = {
            "name": self.name,
            "url": self.url,
            "email": self.email,
        }
        return rv


@attr.s
class License(Serializable):
    # The license name used for the API.
    name: str = attr.ib(validator=required_string)

    # A URL to the license used for the API. MUST be in the format of a URL.
    url: str = attr.ib(default=None, validator=optional_string_as_url)

    def api_format(self):
        rv = {
            "name": self.name,
            "url": self.url,
        }
        return rv


@attr.s
class Server(Serializable):
    # A URL to the target host. This URL supports Server Variables and MAY be
    # relative, to indicate that the host location is relative to the location
    # where the OpenAPI document is being served. Variable substitutions will
    # be made when a variable is named in {brackets}.
    url: str = attr.ib(validator=required_string)

    # An optional string describing the host designated by the URL. CommonMark
    # syntax MAY be used for rich text representation.
    description: str = attr.ib(default=None, validator=optional_string)

    # A map between a variable name and its value. The value is used for
    # substitution in the server's URL template.
    variables: dict = attr.ib(default=None)

    def api_format(self):
        rv = {
            "url": self.url,
            "description": self.description,
            "variables": self.variables,
        }
        return rv


@attr.s
class ServerVariable(Serializable):
    # The default value to use for substitution, which SHALL be sent if an
    # alternate value is not supplied. Note this behavior is different than the
    # Schema Object's treatment of default values, because in those cases
    # parameter values are optional. If the enum is defined, the value SHOULD
    # exist in the enum's values.
    default: str = attr.ib()

    # An enumeration of string values to be used if the substitution options
    # are from a limited set. The array SHOULD NOT be empty.
    enum: list = attr.ib(default=None)

    # An optional description for the server variable. CommonMark syntax MAY
    # be used for rich text representation.
    description: str = attr.ib(default=None)

    def api_format(self):
        rv = {
            "default": self.default,
            "enum": self.enum,
            "description": self.description,
        }
        return rv


@attr.s
class Components(Serializable):
    schemas: dict = attr.ib(default=None)
    responses: dict = attr.ib(default=None)
    parameters: dict = attr.ib(default=None)
    examples: dict = attr.ib(default=None)
    request_bodies: dict = attr.ib(default=None)
    headers: dict = attr.ib(default=None)
    security_schemes: dict = attr.ib(default=None)
    links: dict = attr.ib(default=None)
    callbacks: dict = attr.ib(default=None)

    def api_format(self):
        rv = {
            "schemas": self.schemas,
            "responses": self.responses,
            "parameters": self.parameters,
            "examples": self.examples,
            "requestBodies": self.request_bodies,
            "headers": self.headers,
            "securitySchemes": self.security_schemes,
            "links": self.links,
            "callbacks": self.callbacks,
        }
        return rv


@attr.s
class Paths(Serializable):
    paths = attr.ib()

    def api_format(self):
        rv = {f"/{path.ref}": path for path in self.paths}
        return rv


@attr.s
class Path(Serializable):
    ref: str = attr.ib(default=None)
    summary: str = attr.ib(default=None)
    description: str = attr.ib(default=None)
    get = attr.ib(default=None)
    post = attr.ib(default=None)
    put = attr.ib(default=None)
    options = attr.ib(default=None)
    head = attr.ib(default=None)
    delete = attr.ib(default=None)
    patch = attr.ib(default=None)
    trace = attr.ib(default=None)
    servers = attr.ib(default=None)
    parameters = attr.ib(default=None)

    def api_format(self):
        rv = {
            "summary": self.summary,
            "description": self.description,
            "get": self.get,
            "post": self.post,
            "put": self.put,
            "options": self.options,
            "head": self.head,
            "delete": self.delete,
            "patch": self.patch,
            "trace": self.trace,
            "servers": self.servers,
            "parameters": self.parameters,
        }
        return rv


@attr.s
class Operation(Serializable):
    # The list of possible responses as they are returned from executing this
    # operation.
    responses = attr.ib()

    # A list of tags for API documentation control. Tags can be used for
    # logical grouping of operations by resources or any other qualifier.
    tags: list = attr.ib(default=None)

    # A short summary of what the operation does.
    summary: str = attr.ib(default=None)

    # A verbose explanation of the operation behavior. CommonMark syntax MAY be
    # used for rich text representation.
    description: str = attr.ib(default=None)

    # Unique string used to identify the operation. The id MUST be unique
    # among all operations described in the API. The operationId value is
    # case-sensitive. Tools and libraries MAY use the operationId to uniquely
    # identify an operation, therefore, it is RECOMMENDED to follow common
    # programming naming conventions.
    operation_id: str = attr.ib(default=None)

    # A list of parameters that are applicable for this operation. If a
    # parameter is already defined at the Path Item, the new definition will
    # override it but can never remove it. The list MUST NOT include duplicated
    # parameters. A unique parameter is defined by a combination of a name and
    # location. The list can use the Reference Object to link to parameters
    # that are defined at the OpenAPI Object's components/parameters.
    parameters: list = attr.ib(default=None)

    # Declares this operation to be deprecated. Consumers SHOULD refrain from
    # usage of the declared operation. Default value is false.
    deprecated: bool = attr.ib(default=False)

    # A declaration of which security mechanisms can be used for this operation.
    # The list of values includes alternative security requirement objects that
    # can be used. Only one of the security requirement objects need to be
    # satisfied to authorize a request. To make security optional, an empty
    # security requirement ({}) can be included in the array. This definition
    # overrides any declared top-level security. To remove a top-level security
    # declaration, an empty array can be used.
    security: list = attr.ib(default=None)

    # An alternative server array to service this operation. If an alternative
    # server object is specified at the Path Item Object or Root level, it will
    # be overridden by this value.
    servers: list = attr.ib(default=None)

    # A map of possible out-of band callbacks related to the parent operation.
    # The key is a unique identifier for the Callback Object. Each value in the
    # map is a Callback Object that describes a request that may be initiated
    # by the API provider and the expected responses.
    callbacks: dict = attr.ib(default=None)

    # The request body applicable for this operation. The requestBody is only
    # supported in HTTP methods where the HTTP 1.1 specification RFC7231 has
    # explicitly defined semantics for request bodies. In other cases where the
    # HTTP spec is vague, requestBody SHALL be ignored by consumers.
    request_body = attr.ib(default=None)

    # Additional external documentation for this operation.
    external_docs = attr.ib(default=None)

    def api_format(self):
        rv = {
            "responses": self.responses,
            "tags": self.tags,
            "summary": self.summary,
            "description": self.description,
            "operationId": self.operation_id,
            "parameters": self.parameters,
            "deprecated": self.deprecated,
            "security": self.security,
            "servers": self.servers,
            "callbacks": self.callbacks,
            "requestBody": self.request_body,
            "externalDocs": self.external_docs,
        }
        return rv


@attr.s
class ExternalDocumentation(Serializable):
    # The URL for the target documentation. Value MUST be in the format of a
    # URL.
    url: str = attr.ib()

    # A short description of the target documentation. CommonMark syntax MAY
    # be used for rich text representation.
    description: str = attr.ib(default=None)

    def api_format(self):
        rv = {"url": self.url, "description": self.description}
        return rv


@attr.s
class Parameter(Serializable):
    # The name of the parameter. Parameter names are case sensitive.
    # * If in is "path", the name field MUST correspond to a template
    #   expression occurring within the path field in the Paths Object.
    #   See Path Templating for further information.
    # * If in is "header" and the name field is "Accept", "Content-Type" or
    #   "Authorization", the parameter definition SHALL be ignored.
    # * For all other cases, the name corresponds to the parameter name used
    #   by the in property.
    name: str = attr.ib()

    # The location of the parameter. Possible values are "query", "header",
    # "path" or "cookie".
    in_: str = attr.ib()

    # A brief description of the parameter. This could contain examples of use.
    # CommonMark syntax MAY be used for rich text representation.
    description: str = attr.ib(default=None)

    # Determines whether this parameter is mandatory. If the parameter
    # location is "path", this property is REQUIRED and its value MUST be true.
    # Otherwise, the property MAY be included and its default value is false.
    required: bool = attr.ib(default=True)

    # Specifies that a parameter is deprecated and SHOULD be transitioned out
    # of usage. Default value is false.
    deprecated: bool = attr.ib(default=False)

    # Sets the ability to pass empty-valued parameters. This is valid only for
    # query parameters and allows sending a parameter with an empty value.
    # Default value is false. If style is used, and if behavior is n/a (cannot
    # be serialized), the value of allowEmptyValue SHALL be ignored. Use of
    # this property is NOT RECOMMENDED, as it is likely to be removed in a
    # later revision.
    allow_empty_value: bool = attr.ib(default=False)

    @in_.validator
    def validate_in(self, attribute, value):
        choices = ("query", "header", "path", "cookie")
        if value.lower() not in choices:
            raise ValueError(f"{attribute} must be {choices}")

    def api_format(self):
        rv = {
            "name": self.name,
            "in": self.in_,
            "description": self.description,
            "required": self.required,
            "deprecated": self.deprecated,
            "allowEmptyValue": self.allow_empty_value,
        }
        return rv


@attr.s
class RequestBody(Serializable):
    # The content of the request body. The key is a media type or media type
    # range and the value describes it. For requests that match multiple keys,
    # only the most specific key is applicable.
    # e.g. text/plain overrides text/*
    content: dict = attr.ib()

    # A brief description of the request body. This could contain examples of
    # use. CommonMark syntax MAY be used for rich text representation.
    description: str = attr.ib(default=None)

    # Determines if the request body is required in the request. Defaults to
    # false.
    required: bool = attr.ib(default=True)

    def api_format(self):
        rv = {
            "description": self.description,
            "content": self.content,
            "required": self.required,
        }
        return rv


@attr.s
class MediaType(Serializable):
    # The schema defining the content of the request, response, or parameter.
    schema = attr.ib(default=None)

    # Example of the media type. The example object SHOULD be in the correct
    # format as specified by the media type. The example field is mutually
    # exclusive of the examples field. Furthermore, if referencing a schema
    # which contains an example, the example value SHALL override the example
    # provided by the schema.
    example = attr.ib(default=None)

    # Examples of the media type. Each example object SHOULD match the media
    # type and specified schema if present. The examples field is mutually
    # exclusive of the example field. Furthermore, if referencing a schema
    # which contains an example, the examples value SHALL override the example
    # provided by the schema.
    examples: dict = attr.ib(default=None)

    # A map between a property name and its encoding information. The key,
    # being the property name, MUST exist in the schema as a property. The
    # encoding object SHALL only apply to requestBody objects when the media
    # type is multipart or application/x-www-form-urlencoded.
    encoding: dict = attr.ib(default=None)

    def api_format(self):
        rv = {
            "schema": self.schema,
            "example": self.example,
            "examples": self.examples,
            "encoding": self.encoding,
        }
        return rv


@attr.s
class Encoding(Serializable):
    # The Content-Type for encoding a specific property. Default value depends
    # on the property type: for string with format being binary –
    # application/octet-stream; for other primitive types – text/plain; for
    # object - application/json; for array – the default is defined based on
    # the inner type. The value can be a specific media type
    # (e.g. application/json), a wildcard media type (e.g. image/*), or a
    # comma-separated list of the two types.
    content_type: str = attr.ib(default=None)

    # A map allowing additional information to be provided as headers, for
    # example Content-Disposition. Content-Type is described separately and
    # SHALL be ignored in this section. This property SHALL be ignored if the
    # request body media type is not a multipart.
    headers: dict = attr.ib(default=None)

    # Describes how a specific property value will be serialized depending on
    # its type. See Parameter Object for details on the style property. The
    # behavior follows the same values as query parameters, including default
    # values. This property SHALL be ignored if the request body media type is
    # not application/x-www-form-urlencoded.
    style: str = attr.ib(default=None)

    # When this is true, property values of type array or object generate
    # separate parameters for each value of the array, or key-value-pair of
    # the map. For other types of properties this property has no effect.
    # When style is form, the default value is true. For all other styles,
    # the default value is false. This property SHALL be ignored if the request
    # body media type is not application/x-www-form-urlencoded.
    explode: bool = attr.ib(default=True)

    # Determines whether the parameter value SHOULD allow reserved characters,
    # as defined by RFC3986 :/?#[]@!$&'()*+,;= to be included without
    # percent-encoding. The default value is false. This property SHALL be
    # ignored if the request body media type is not
    # application/x-www-form-urlencoded.
    allow_reserved: bool = attr.ib(default=False)

    def api_format(self):
        rv = {
            "contentType": self.content_type,
            "headers": self.headers,
            "style": self.style,
            "explode": self.explode,
            "allowReserved": self.allow_reserved,
        }
        return rv


@attr.s
class Responses(Serializable):
    # Any HTTP status code can be used as the property name, but only one
    # property per code, to describe the expected response for that HTTP status
    # code. A Reference Object can link to a response that is defined in the
    # OpenAPI Object's components/responses section. This field MUST be
    # enclosed in quotation marks (for example, "200") for compatibility
    # between JSON and YAML. To define a range of response codes, this field
    # MAY contain the uppercase wildcard character X. For example, 2XX
    # represents all response codes between [200-299]. Only the following
    # range definitions are allowed: 1XX, 2XX, 3XX, 4XX, and 5XX. If a response
    # is defined using an explicit code, the explicit code definition takes
    # precedence over the range definition for that code.
    responses = attr.ib(default=None)

    # The documentation of responses other than the ones declared for specific
    # HTTP response codes. Use this field to cover undeclared responses. A
    # Reference Object can link to a response that the OpenAPI Object's
    # components/responses section defines.
    # todo fix this
    default = attr.ib(factory=list)

    @default.validator
    def validate_default(self, attribute, value):
        # todo fix this
        if "default" in self.responses and value is not None:
            raise ValueError(
                "You must put default as a attribute or as a response, " "not both."
            )

    def api_format(self):
        # todo fix with above
        responses = self.default + self.responses
        # responses = self.responses.copy()
        # if "default" not in responses:
        #     responses.update({"default": self.default})

        rv = {response.status_code: response for response in responses}
        return rv


@attr.s
class Response(Serializable):
    # A short description of the response. CommonMark syntax MAY be used for
    # rich text representation.
    description: str = attr.ib()

    # ADDED TO OBJECT
    status_code = attr.ib(default=None)

    # Maps a header name to its definition. RFC7230 states header names are
    # case insensitive. If a response header is defined with the name
    # "Content-Type", it SHALL be ignored.
    headers: dict = attr.ib(default=None)

    # Maps a header name to its definition. RFC7230 states header names are
    # case insensitive. If a response header is defined with the name
    # "Content-Type", it SHALL be ignored.
    content: dict = attr.ib(default=None)

    # A map of operations links that can be followed from the response. The key
    # of the map is a short name for the link, following the naming constraints
    # of the names for Component Objects.
    links: dict = attr.ib(default=None)

    def api_format(self):
        rv = {
            "description": self.description,
            "headers": self.headers,
            "content": self.content,
            "links": self.links,
        }
        return rv


@attr.s
class Callback(Serializable):
    # A Path Item Object used to define a callback request and expected
    # responses. A complete example is available.
    expression = attr.ib(default=None)

    def api_format(self):
        rv = {"expression": self.expression}
        return rv


@attr.s
class Example(Serializable):
    # Short description for the example.
    summary: str = attr.ib(default=None)

    # Long description for the example. CommonMark syntax MAY be used for rich
    # text representation.
    description: str = attr.ib(default=None)

    # Embedded literal example. The value field and externalValue field are
    # mutually exclusive. To represent examples of media types that cannot
    # naturally represented in JSON or YAML, use a string value to contain the
    # example, escaping where necessary.
    value = attr.ib(default=None)

    # A URL that points to the literal example. This provides the capability to
    # reference examples that cannot easily be included in JSON or YAML
    # documents. The value field and externalValue field are mutually exclusive.
    external_value: str = attr.ib(default=None)

    def api_format(self):
        rv = {
            "summary": self.summary,
            "description": self.description,
            "value": self.value,
            "externalValue": self.external_value,
        }
        return rv


@attr.s
class Link(Serializable):
    # A relative or absolute URI reference to an OAS operation. This field is
    # mutually exclusive of the operationId field, and MUST point to an
    # Operation Object. Relative operationRef values MAY be used to locate an
    # existing Operation Object in the OpenAPI definition.
    operation_ref: str = attr.ib(default=None)

    # The name of an existing, resolvable OAS operation, as defined with a
    # unique operationId. This field is mutually exclusive of the operationRef
    # field.
    operation_id: str = attr.ib(default=None)

    # A map representing parameters to pass to an operation as specified with
    # operationId or identified via operationRef. The key is the parameter name
    # to be used, whereas the value can be a constant or an expression to be
    # evaluated and passed to the linked operation. The parameter name can be
    # qualified using the parameter location [{in}.]{name} for operations that
    # use the same parameter name in different locations (e.g. path.id).
    parameters: dict = attr.ib(default=None)

    # A literal value or {expression} to use as a request body when calling the
    # target operation.
    request_body = attr.ib(default=None)

    # A description of the link. CommonMark syntax MAY be used for rich text
    # representation.
    description: str = attr.ib(default=None)

    # A server object to be used by the target operation.
    server: str = attr.ib(default=None)

    def api_format(self):
        rv = {
            "operationRef": self.operation_ref,
            "operationId": self.operation_id,
            "parameters": self.parameters,
            "requestBody": self.request_body,
            "description": self.description,
            "server": self.server,
        }
        return rv


# @attr.s
# class Header(Serializable):
#     description: str = attr.ib(default=None)
#     required: bool = attr.ib(default=True)
#     deprecated: bool = attr.ib(default=False)
#     allow_empty_value: bool = attr.ib(default=False)
#
#     def api_format(self):
#         rv = {
#             "description": self.description,
#             "required": self.required,
#             "deprecated": self.deprecated,
#             "allowEmptyValue": self.allow_empty_value
#         }
#         return rv


@attr.s
class Tag(Serializable):
    # The name of the tag.
    name: str = attr.ib()

    # A short description for the tag. CommonMark syntax MAY be used for rich
    # text representation.
    description: str = attr.ib(default=None)

    # Additional external documentation for this tag.
    external_docs = attr.ib(default=None)

    def api_format(self):
        rv = {
            "name": self.name,
            "description": self.description,
            "external_docs": self.external_docs,
        }
        return rv


@attr.s
class Reference(Serializable):
    # The reference string.
    ref: str = attr.ib()

    def api_format(self):
        return {"$ref": self.ref}


@attr.s
class Schema(Serializable):
    title: str = attr.ib(default=None)
    multiple_of = attr.ib(default=None)
    maximum = attr.ib(default=None)
    exclusive_maximum = attr.ib(default=None)
    minimum = attr.ib(default=None)
    exclusive_minimum = attr.ib(default=None)
    max_length = attr.ib(default=None)
    min_length = attr.ib(default=None)
    pattern = attr.ib(default=None)
    max_items = attr.ib(default=None)
    min_items = attr.ib(default=None)
    unique_items = attr.ib(default=None)
    max_properties = attr.ib(default=None)
    required = attr.ib(default=None)
    enum = attr.ib(default=None)

    type: str = attr.ib(default=None)
    all_of = attr.ib(default=None)
    one_of = attr.ib(default=None)
    any_of = attr.ib(default=None)
    not_ = attr.ib(default=None)
    items = attr.ib(default=None)
    properties = attr.ib(default=None)
    additional_properties = attr.ib(default=True)
    description = attr.ib(default=None)
    format = attr.ib(default=None)
    default = attr.ib(default=None)

    nullable: bool = attr.ib(default=False)
    discriminator = attr.ib(default=None)
    read_only: bool = attr.ib(default=False)
    write_only: bool = attr.ib(default=False)
    xml = attr.ib(default=None)
    external_docs = attr.ib(default=None)
    example = attr.ib(default=None)
    deprecated: bool = attr.ib(default=False)

    def api_format(self):
        def snake_to_camel(word):
            a, *b = word.split("_")
            return a + "".join(c.title() for c in b)

        rv = {
            snake_to_camel(i): j
            for i, j in vars(self).items()
        }
        return rv


@attr.s
class Discriminator(Serializable):
    # The name of the property in the payload that will hold the discriminator
    # value.
    property_name: str = attr.ib()

    # An object to hold mappings between payload values and schema names or
    # references.
    mapping: dict = attr.ib(default=None)

    def api_format(self):
        # todo this might not be right
        return {"propertyName": self.property_name, "mapping": self.mapping}


@attr.s
class XML(Serializable):
    # Replaces the name of the element/attribute used for the described schema
    # property. When defined within items, it will affect the name of the
    # individual XML elements within the list. When defined alongside type
    # being array (outside the items), it will affect the wrapping element and
    # only if wrapped is true. If wrapped is false, it will be ignored.
    name: str = attr.ib(default=None)

    # The URI of the namespace definition. Value MUST be in the form of an
    # absolute URI.
    namespace: str = attr.ib(default=None)

    # The prefix to be used for the name.
    prefix: str = attr.ib(default=None)

    # Declares whether the property definition translates to an attribute
    # instead of an element. Default value is false.
    attribute: str = attr.ib(default=None)

    # MAY be used only for an array definition. Signifies whether the array is
    # wrapped (for example, <books><book/><book/></books>) or unwrapped
    # (<book/><book/>). Default value is false. The definition takes effect
    # only when defined alongside type being array (outside the items).
    wrapped: bool = attr.ib(default=False)

    def api_format(self):
        # todo this might not be right
        rv = {
            "name": self.name,
            "namespace": self.namespace,
            "prefix": self.prefix,
            "attribute": self.attribute,
            "wrapped": self.wrapped
        }
        return rv


@attr.s
class SecurityScheme(Serializable):
    # The type of the security scheme. Valid values are "apiKey", "http",
    # "oauth2", "openIdConnect".
    type: str = attr.ib()

    @type.validator
    def validate_type(self, attribute, value):
        allowed = ("apiKey", "http", "oauth2", "openIdConnect")
        if value not in allowed:
            raise ValueError(f"{attribute} must be in {allowed}")

    # The name of the header, query or cookie parameter to be used.
    name: str = attr.ib()

    # The location of the API key. Valid values are "query", "header" or
    # "cookie".
    in_: str = attr.ib()

    @in_.validator
    def validate_in(self, attribute, value):
        allowed = ("query", "header", "cookie")
        if value not in allowed:
            raise ValueError(f"{attribute} must be in {allowed}")

    # The name of the HTTP Authorization scheme to be used in the Authorization
    # header as defined in RFC7235. The values used SHOULD be registered in the
    # IANA Authentication Scheme registry.
    scheme: str = attr.ib()

    # An object containing configuration information for the flow types
    # supported.
    flows = attr.ib()

    # OpenId Connect URL to discover OAuth2 configuration values. This MUST be
    # in the form of a URL.
    open_id_connect_url: str = attr.ib()

    # A short description for security scheme. CommonMark syntax MAY be used
    # for rich text representation.
    description: str = attr.ib(default=None)

    # A hint to the client to identify how the bearer token is formatted.
    # Bearer tokens are usually generated by an authorization server, so this
    # information is primarily for documentation purposes.
    bearer_format: str = attr.ib(default=None)

    def api_format(self):
        rv = {
            "type": self.type,
            "name": self.name,
            "in": self.in_,
            "scheme": self.scheme,
            "openIdConnectUrl": self.open_id_connect_url,
            "description": self.description,
            "bearerFormat": self.bearer_format,
        }
        return rv


@attr.s
class OAuthFlows(Serializable):
    # Configuration for the OAuth Implicit flow
    implicit = attr.ib(default=None)

    # Configuration for the OAuth Resource Owner Password flow
    password = attr.ib(default=None)

    # Configuration for the OAuth Client Credentials flow. Previously called
    # application in OpenAPI 2.0.
    client_credentials = attr.ib(default=None)

    # Configuration for the OAuth Authorization Code flow. Previously called
    # accessCode in OpenAPI 2.0.
    authorization_code = attr.ib(default=None)

    def api_format(self):
        rv = {
            "implicit": self.implicit,
            "password": self.password,
            "clientCredentials": self.client_credentials,
            "scheme": self.scheme,
            "authorizationCode": self.authorization_code,
        }
        return rv


@attr.s
class OAuthFlow(Serializable):
    # The authorization URL to be used for this flow. This MUST be in the form
    # of a URL.
    authorization_url: str = attr.ib()

    # The token URL to be used for this flow. This MUST be in the form of a URL.
    token_url: str = attr.ib()

    # REQUIRED. The available scopes for the OAuth2 security scheme. A map
    # between the scope name and a short description for it. The map MAY be
    # empty.
    scopes: dict = attr.ib()

    # The URL to be used for obtaining refresh tokens. This MUST be in the
    # form of a URL.
    refresh_url: str = attr.ib(default=None)

    def api_format(self):
        rv = {
            "authorizationUrl": self.authorization_url,
            "tokenUrl": self.token_url,
            "scopes": self.scopes,
            "refreshUrl": self.refresh_url,
        }
        return rv


@attr.s
class SecurityRequirement(Serializable):
    # Each name MUST correspond to a security scheme which is declared in the
    # Security Schemes under the Components Object. If the security scheme is
    # of type "oauth2" or "openIdConnect", then the value is a list of scope
    # names required for the execution, and the list MAY be empty if
    # authorization does not require a specified scope. For other security
    # scheme types, the array MUST be empty.
    name: dict = attr.ib()

    def api_format(self):
        return self.name
