"""JSON parser tests"""
from typing import Dict
import pytest

import json_parser


@pytest.mark.parametrize(
    ('json_string', 'expected'),
    (
        ('{}', {}),
        ('[]', []),
        ('{"abc": "def"}', {"abc": "def"}),
        ('{"value": 42}', {"value": 42}),
        ('{"value": 12.3}', {"value": 12.3}),
        ('["foo", "bar"]', ["foo", "bar"]),
        ('[1, 2, 3]', [1, 2, 3]),
        ('{"value1": true, "value2": false, "value3": null}',
         {"value1": True, "value2": False, "value3": None}),
        ('{"foo": [1, 2, {"bar": 3}]}', {"foo": [1, 2, {"bar": 3}]}),
    )
)
def test_parser(json_string: str, expected: Dict[str, object]) -> None:
    """JSON parser tests"""
    assert json_parser.parse(json_string) == expected
