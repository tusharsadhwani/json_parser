"""Parser functions"""
from typing import Dict, List, Union

from json_parser.lexer import tokenize

JSONArray = List[object]
JSONObject = Dict[str, object]
JSONNumber = Union[int, float]


class ParseError(Exception):
    """Error thrown when an invalid JSON tokens is parsed"""


def parse_object(tokens: List[str]) -> JSONObject:
    """Parses an object out of json tokens"""
    obj: JSONObject = {}

    # special case:
    if tokens[0] == '}':
        tokens.pop(0)
        return obj

    while tokens:
        token = tokens.pop(0)

        # least amount of tokens left shouldif be a colon, a token and a }
        if len(tokens) < 3:
            raise ParseError("Unexpected end of file while parsing")

        if not token.startswith('"'):
            raise ParseError(
                "Expected string key for object, found {}".format(token))

        key = parse_string(token)

        token = tokens.pop(0)
        if token != ':':
            raise ParseError("Expected colon, found {}".format(token))

        value = _parse(tokens)
        obj[key] = value

        if not tokens:
            raise ParseError("Unexpected end of file while parsing")

        token = tokens.pop(0)
        if token not in ',}':
            raise ParseError("Expected ',' or '}}', found {}".format(token))

        if token == '}':
            break

    return obj


def parse_array(tokens: List[str]) -> JSONArray:
    """Parses an array out of json tokens"""
    array: JSONArray = []

    # special case:
    if tokens[0] == ']':
        tokens.pop(0)
        return array

    while tokens:
        # least number of tokens left should be a token and a ]
        if len(tokens) < 2:
            raise ParseError("Unexpected end of file while parsing")

        value = _parse(tokens)
        array.append(value)

        token = tokens.pop(0)
        if token not in ',]':
            raise ParseError("Expected ',' or ']', found {}".format(token))

        if token == ']':
            break

    return array


def parse_string(token: str) -> str:
    """Parses a string out of a json token"""
    return token[1:-1]


def parse_number(token: str) -> JSONNumber:
    """Parses a number out of a json token"""
    try:
        if token.isdigit():
            number: JSONNumber = int(token)
        else:
            number = float(token)
        return number

    except ValueError as err:
        raise ParseError("Invalid token: {}".format(token)) from err


def _parse(tokens: List[str]) -> object:
    """Recursive JSON parse implementation"""
    token = tokens.pop(0)

    if token == '[':
        return parse_array(tokens)

    if token == '{':
        return parse_object(tokens)

    if token.startswith('"'):
        return parse_string(token)

    if token[0].isdigit():
        return parse_number(token)

    special_tokens = {
        'true': True,
        'false': False,
        'null': None,
    }
    if token in special_tokens:
        return special_tokens[token]

    raise ParseError("Unexpected token: {}".format(token))


def parse(json_string: str) -> object:
    """Parses a json string into a Python object"""
    tokens = tokenize(json_string)

    value = _parse(tokens)
    if len(tokens) != 0:
        raise ParseError("Invalid JSON at {}".format(tokens[0]))

    return value


parse('["foo", "bar"]')
