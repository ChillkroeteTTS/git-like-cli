import json
import os
from os.path import expanduser

CONFIG_PATH = '.gitlike'


class Config(object):
    email: str
    code: str
    lastChecked: str


def config_is_valid() -> bool:
    config = read_config()
    email = config['email']
    code = config['code']
    email_is_valid = len(email) > 0 and "@" in email
    code_is_valid = len(code) > 0
    return email_is_valid and code_is_valid


def read_config() -> Config:
    with open(get_config_path(), 'r') as f:
        return json.loads(f.read())


def write_config(partial):
    if os.path.isfile(get_config_path()):
        config = {**read_config(), **partial}
    else:
        config = partial

    with open(get_config_path(), 'w+') as f:
        f.write(json.dumps(config))


def get_config_path() -> str:
    return expanduser("~") + '/' + CONFIG_PATH

