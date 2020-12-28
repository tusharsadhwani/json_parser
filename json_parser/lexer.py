"""Lexer functions"""
from collections import deque
import string
from typing import Deque


class TokenizeError(Exception):
    """Error thrown when an invalid JSON string is tokenized"""


def extract_string(json_string: str, index: int, tokens: Deque[str]) -> int:
    """Extracts a single string token from JSON string"""
    start = index
    end = len(json_string)
    index += 1

    while index < end:
        char = json_string[index]
        if char == '"':
            index += 1
            string_token = json_string[start:index]
            tokens.append(string_token)
            return index

        index += 1

    raise TokenizeError("Expected end of string")


def extract_number(json_string: str, index: int, tokens: Deque[str]) -> int:
    """Extracts a single number token (eg. 42, -12.3) from JSON string"""
    start = index
    end = len(json_string)

    leading_minus_found = False
    decimal_point_found = False

    while index < end:
        char = json_string[index]
        if char == '.':
            if decimal_point_found:
                raise TokenizeError("Too many decimal points in number")

            decimal_point_found = True

        elif char == '-':
            if leading_minus_found:
                raise TokenizeError("Minus sign in between number")

            leading_minus_found = True

        elif not char.isdigit():
            string_token = json_string[start:index]
            tokens.append(string_token)
            return index

        index += 1

    return index


def extract_special(json_string: str, index: int, tokens: Deque[str]) -> int:
    """Extracts true, false and null from JSON string"""
    end = len(json_string)

    word = ''
    while index < end:
        char = json_string[index]
        if not char.isalpha():
            break

        word += char
        index += 1

    if word in ('true', 'false', 'null'):
        tokens.append(word)
        return index

    raise TokenizeError(f"Unknown token found: {word}")


def tokenize(json_string: str) -> Deque[str]:
    """Converts a JSON string into a queue of tokens"""
    tokens: Deque[str] = deque()

    index = 0
    end = len(json_string)
    while index < end:
        char = json_string[index]

        if char in string.whitespace:
            index += 1

        elif char in '[]{}:,':
            tokens.append(char)
            index += 1

        elif char == '"':
            index = extract_string(json_string, index, tokens)

        elif char == '-' or char.isdigit():
            index = extract_number(json_string, index, tokens)

        else:
            index = extract_special(json_string, index, tokens)

    return tokens
