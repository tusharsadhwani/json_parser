"""JSON parser tests"""
from typing import Dict
import pytest

import json_parser


@pytest.mark.parametrize(
    ('json_string', 'expected'),
    (
        ('{}', {}),
        ('[]', []),
    )
)
def test_parser(json_string: str, expected: Dict[str, object]) -> None:
    """JSON parser tests"""
    assert json_parser.parse(json_string) == expected
