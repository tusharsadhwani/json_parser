"""Parser functions"""
from ast import literal_eval
from typing import Deque, Dict, List, Union

from json_parser.lexer import tokenize

JSONArray = List[object]
JSONObject = Dict[str, object]
JSONNumber = Union[int, float]


class ParseError(Exception):
    """Error thrown when invalid JSON tokens are parsed"""


def parse_object(tokens: Deque[str]) -> JSONObject:
    """Parses an object out of JSON tokens"""
    obj: JSONObject = {}

    # special case:
    if tokens[0] == '}':
        tokens.popleft()
        return obj

    while tokens:
        token = tokens.popleft()

        # least amount of tokens left should be a colon, a token and a }
        if len(tokens) < 3:
            raise ParseError("Unexpected end of file while parsing")

        if not token.startswith('"'):
            raise ParseError(f"Expected string key for object, found {token}")

        key = parse_string(token)

        token = tokens.popleft()
        if token != ':':
            raise ParseError(f"Expected colon, found {token}")

        value = _parse(tokens)
        obj[key] = value

        if not tokens:
            raise ParseError("Unexpected end of file while parsing")

        token = tokens.popleft()
        if token not in ',}':
            raise ParseError(f"Expected ',' or '}}', found {token}")

        if token == '}':
            break

    return obj


def parse_array(tokens: Deque[str]) -> JSONArray:
    """Parses an array out of JSON tokens"""
    array: JSONArray = []

    # special case:
    if tokens[0] == ']':
        tokens.popleft()
        return array

    while tokens:
        # least number of tokens left should be a token and a ]
        if len(tokens) < 2:
            raise ParseError("Unexpected end of file while parsing")

        value = _parse(tokens)
        array.append(value)

        token = tokens.popleft()
        if token not in ',]':
            raise ParseError(f"Expected ',' or ']', found {token}")

        if token == ']':
            break

        # trailing comma check
        if tokens[0] == ']':
            raise ParseError("Expected value after comma, found ]")

    return array


def parse_string(token: str) -> str:
    """Parses a string out of a JSON token"""
    chars: List[str] = []

    index = 1
    end = len(token) - 1
    while index < end:
        char = token[index]

        if char != '\\':
            chars.append(char)
            index += 1
            continue

        next_char = token[index+1]
        if next_char == 'u':
            hex_string = token[index+2:index+6]
            try:
                unicode_char = literal_eval(f'"\\u{hex_string}"')
            except ValueError as err:
                raise ParseError(f"Invalid escape: \\u{hex_string}") from err

            chars.append(unicode_char)
            index += 6
            continue

        if next_char in '"\\/':
            chars.append(next_char)
        elif next_char == 'b':
            chars.append('\b')
        elif next_char == 'f':
            chars.append('\f')
        elif next_char == 'n':
            chars.append('\n')
        elif next_char == 'r':
            chars.append('\r')
        elif next_char == 't':
            chars.append('\t')
        else:
            raise ParseError(f"Unknown escape sequence found in {token}")

        index += 2

    string = ''.join(chars)
    return string


def parse_number(token: str) -> JSONNumber:
    """Parses a number out of a JSON token"""
    try:
        if token.isdigit():
            number: JSONNumber = int(token)
        else:
            number = float(token)
        return number

    except ValueError as err:
        raise ParseError(f"Invalid token: {token}") from err


def _parse(tokens: Deque[str]) -> object:
    """Recursive JSON parse implementation"""
    token = tokens.popleft()

    if token == '[':
        return parse_array(tokens)

    if token == '{':
        return parse_object(tokens)

    if token.startswith('"'):
        return parse_string(token)

    if token[0] == '-' or token[0].isdigit():
        return parse_number(token)

    special_tokens = {
        'true': True,
        'false': False,
        'null': None,
    }
    if token in special_tokens:
        return special_tokens[token]

    raise ParseError(f"Unexpected token: {token}")


def parse(json_string: str) -> object:
    """Parses a JSON string into a Python object"""
    tokens = tokenize(json_string)

    value = _parse(tokens)
    if len(tokens) != 0:
        raise ParseError(f"Invalid JSON at {tokens[0]}")

    return value
