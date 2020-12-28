# json_parser

An _efficient_ JSON parser written in Python.

## Installation

Install it via pip:

```console
pip install json-parser
```

## Usage

```py
import json_parser

data = json_parser.parse('{"value": 42}')
print(data['value']) # 42
```

## Testing

Clone the app and run the following:

```console
pip install -e .
pytest
```
