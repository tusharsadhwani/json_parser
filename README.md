# json_parser

An _efficient_ JSON parser written in Python.

## usage

```py
import json_parser

json_object = json_parser.parse('{"value": 42}')
print(json_object['value']) # 42
```
