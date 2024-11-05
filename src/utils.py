import json
from typing import Any


def write_json(filepath: str, data: Any):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)


def read_json(filepath: str) -> Any:
    with open(filepath, 'r') as f:
        return json.load(f)
