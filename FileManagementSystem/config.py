import json

class CONFIG(dict):
    def __init__(self):
        super().__init__(read_json('config.json'))


def read_json(file: str = 'config.json') -> dict:
    with open(file) as f:
        return json.load(f)

