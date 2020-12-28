"""JSON parser tests"""
from typing import List

import pytest

import json_parser.lexer
from json_parser.lexer import TokenizeError


@pytest.mark.parametrize(
    ('json_string', 'expected'),
    (
        ('""', ['""']),
        ('"abc"', ['"abc"']),
        ('42', ['42']),
        ('{}', ['{', '}']),
        ('{"abc": "def"}', ['{', '"abc"', ':', '"def"', '}']),
        ('{"value": 42}', ['{', '"value"', ':', '42', '}']),
        ('{"value": 12.3}', ['{', '"value"', ':', '12.3', '}']),
        ('[]', ['[', ']']),
        ('["foo", "bar"]', ['[', '"foo"', ',', '"bar"', ']']),
        ('[1, 2, 3, "abc"]', ['[', '1', ',', '2', ',', '3', ',', '"abc"', ']']),
        ('{"value": true}', ['{', '"value"', ':', 'true', '}']),
        ('{"value": false}', ['{', '"value"', ':', 'false', '}']),
        ('{"value": null}', ['{', '"value"', ':', 'null', '}']),
        ('{"foo": [1, 2, {"bar": 3}]}',
         ['{', '"foo"', ':', '[', '1', ',', '2', ',', '{', '"bar"', ':', '3', '}', ']', '}']),
    )
)
def test_lexer(json_string: str, expected: List[str]) -> None:
    """JSON lexer tests"""
    assert list(json_parser.lexer.tokenize(json_string)) == expected


@pytest.mark.parametrize(
    ('json_string', 'error_message'),
    (
        ('', 'Cannot parse empty string'),
        ('blabla', 'Unknown token found: blabla'),
        ('"abc', 'Expected end of string'),
        ('"abc\\"', 'Expected end of string'),
        ('["a", "b", c]', 'Unknown token found: c'),
    )
)
def test_lexer_failure(json_string: str, error_message: str) -> None:
    """JSON lexer test failutes"""
    with pytest.raises(TokenizeError) as exinfo:
        json_parser.lexer.tokenize(json_string)

    msg, = exinfo.value.args
    assert msg == error_message
