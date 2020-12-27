"""JSON parser tests"""
from typing import List
import pytest

import json_parser.lexer


@pytest.mark.parametrize(
    ('json_string', 'expected'),
    (
        ('{}', ['{', '}']),
        ('{"abc": "def"}', ['{', '"abc"', ':', '"def"', '}']),
        ('{"value": 42}', ['{', '"value"', ':', '42', '}']),
        ('{"value": 12.3}', ['{', '"value"', ':', '12.3', '}']),
        ('["foo", "bar"]', ['[', '"foo"', ',', '"bar"', ']']),
        ('[1, 2, 3]', ['[', '1', ',', '2', ',', '3', ']']),
        ('{"value": true}', ['{', '"value"', ':', 'true', '}']),
        ('{"value": false}', ['{', '"value"', ':', 'false', '}']),
        ('{"value": null}', ['{', '"value"', ':', 'null', '}']),
        ('{"foo": [1, 2, {"bar": 3}]}',
         ['{', '"foo"', ':', '[', '1', ',', '2', ',', '{', '"bar"', ':', '3', '}', ']', '}']),
    )
)
def test_lexer(json_string: str, expected: List[str]) -> None:
    """JSON lexer tests"""
    assert json_parser.lexer.tokenize(json_string) == expected
