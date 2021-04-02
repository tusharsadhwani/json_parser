# json_parser

An _efficient_ JSON parser written in Python.

## Installation

Install it via pip:

```bash
pip install json-parser
```

## Usage

```python
import json_parser

data = json_parser.parse('{"value": 42}')
print(data['value']) # 42
```

## Benchmarks

Running it on [this 25MB JSON file][1] gave the following results:

```pycon
>>> with open('large-file.json') as f:
...   t = time.time()
...   x = json.load(f)
...   t = time.time() - t
...   print(t, 'seconds')
...
0.6405608654022217 seconds
>>> with open('large-file.json') as f:
...   t = time.time()
...   y = json_parser.parse(f.read())
...   t = time.time() - t
...   print(t, 'seconds')
...
22.286625385284424 seconds
>>> x == y
True
```

So, it's about 34x slower than the builtin `json`.
Which, is par for the course when it comes to pure python.

## Testing

Clone the app and run the following:

```bash
pip install -e '.[dev]'
pytest
```

[1]: https://raw.githubusercontent.com/json-iterator/test-data/master/large-file.json
