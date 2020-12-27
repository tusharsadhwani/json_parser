"""Parser functions"""
from typing import Dict

from .lexer import tokenize


def parse(json_string: str) -> Dict[str, object]:
    """Parses a json string into a dictionary"""
    tokens = tokenize(json_string)

    print(tokens)  # TODO: parse

    return {}
