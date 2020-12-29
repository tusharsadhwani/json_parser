"""Parser functions"""
from ast import literal_eval
from typing import Deque, Dict, List, Union

from json_parser.lexer import Token, tokenize

JSONArray = List[object]
JSONObject = Dict[str, object]
JSONNumber = Union[int, float]


class ParseError(Exception):
    """Error thrown when invalid JSON tokens are parsed"""


def parse_object(tokens: Deque[Token]) -> JSONObject:
    """Parses an object out of JSON tokens"""
    obj: JSONObject = {}

    # special case:
    if tokens[0].type == 'right_brace':
        tokens.popleft()
        return obj

    while tokens:
        token = tokens.popleft()

        if not token.type == 'string':
            raise ParseError(
                f"Expected string key for object, found {token.value}")

        key = parse_string(token)

        if len(tokens) == 0:
            raise ParseError("Unexpected end of file while parsing")

        token = tokens.popleft()
        if token.type != 'colon':
            raise ParseError(f"Expected colon, found {token.value}")

        # Missing value for key
        if len(tokens) == 0:
            raise ParseError("Unexpected end of file while parsing")

        if tokens[0].type == 'right_brace':
            raise ParseError("Expected value after colon, found }")

        value = _parse(tokens)
        obj[key] = value

        if len(tokens) == 0:
            raise ParseError("Unexpected end of file while parsing")

        token = tokens.popleft()
        if token.type not in ('comma', 'right_brace'):
            raise ParseError(f"Expected ',' or '}}', found {token.value}")

        if token.type == 'right_brace':
            break

        # Trailing comma check
        if len(tokens) == 0:
            raise ParseError("Unexpected end of file while parsing")

        if tokens[0].type == 'right_brace':
            raise ParseError("Expected value after comma, found }")

    return obj


def parse_array(tokens: Deque[Token]) -> JSONArray:
    """Parses an array out of JSON tokens"""
    array: JSONArray = []

    # special case:
    if tokens[0].type == 'right_bracket':
        tokens.popleft()
        return array

    while tokens:
        # least number of tokens left should be a token and a ]
        if len(tokens) < 2:
            raise ParseError("Unexpected end of file while parsing")

        value = _parse(tokens)
        array.append(value)

        token = tokens.popleft()
        if token.type not in ('comma', 'right_bracket'):
            raise ParseError(f"Expected ',' or ']', found {token.value}")

        if token.type == 'right_bracket':
            break

        # trailing comma check
        if len(tokens) == 0:
            raise ParseError("Unexpected end of file while parsing")

        if tokens[0].type == 'right_bracket':
            raise ParseError("Expected value after comma, found ]")

    return array


def parse_string(token: Token) -> str:
    """Parses a string out of a JSON token"""
    chars: List[str] = []

    index = 1
    end = len(token.value) - 1
    while index < end:
        char = token.value[index]

        if char != '\\':
            chars.append(char)
            index += 1
            continue

        next_char = token.value[index+1]
        if next_char == 'u':
            hex_string = token.value[index+2:index+6]
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
            raise ParseError(f"Unknown escape sequence found in {token.value}")

        index += 2

    string = ''.join(chars)
    return string


def parse_number(token: Token) -> JSONNumber:
    """Parses a number out of a JSON token"""
    try:
        if token.value.isdigit():
            number: JSONNumber = int(token.value)
        else:
            number = float(token.value)
        return number

    except ValueError as err:
        raise ParseError(f"Invalid token: {token.value}") from err


def _parse(tokens: Deque[Token]) -> object:
    """Recursive JSON parse implementation"""
    token = tokens.popleft()

    if token.type == 'left_bracket':
        return parse_array(tokens)

    if token.type == 'left_brace':
        return parse_object(tokens)

    if token.type == 'string':
        return parse_string(token)

    if token.type == 'number':
        return parse_number(token)

    special_tokens = {
        'true': True,
        'false': False,
        'null': None,
    }
    if token.type in ('boolean', 'null'):
        return special_tokens[token.value]

    raise ParseError(f"Unexpected token: {token.value}")


def parse(json_string: str) -> object:
    """Parses a JSON string into a Python object"""
    tokens = tokenize(json_string)

    value = _parse(tokens)
    if len(tokens) != 0:
        raise ParseError(f"Invalid JSON at {tokens[0].value}")

    return value
