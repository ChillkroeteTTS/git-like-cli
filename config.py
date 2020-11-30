import json
from os.path import expanduser

CONFIG_PATH = '.codelike'


class Config(object):
    email: str
    code: str


def read_config() -> Config:
    with open(expanduser("~") + CONFIG_PATH, 'r') as f:
        return json.loads(f.read())

def write_config(partial):
    config = {**read_config(), **partial}

    with open(expanduser("~") + CONFIG_PATH, 'w+') as f:
        f.write(json.dumps(config))

