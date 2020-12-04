import json
import re
from os.path import expanduser
from pprint import pprint

import click
import requests
from git import Repo

from gitlike.config import read_config


def get_api_key():
    return 'GwHQ9OUXum5EilDTmGJJB4nnFSEaKBle76DvSNz7'


def get_current_git_user():
    with open(expanduser("~") + '/.gitconfig', 'r') as f:
        lines = [l for l in f.readlines() if 'email' in l]

    if (len(lines) > 0):
        email = re.search('=\s*(.*)$', lines[0]).group(1)
        return email
    else:
        print('Could not find gitconfig with email', lines)

def get_repo():
    return Repo(search_parent_directories=True)


def get_likes(last_checked=None):
    config = read_config()

    # self.logger.info(self.lastChecked + ' ' + user)
    payload = {
        'user': get_current_git_user(),
        'code': config['code']
    }
    if last_checked is not None:
        payload['lastChecked'] = last_checked
    r = requests.post('https://1nvgpilww4.execute-api.eu-central-1.amazonaws.com/dev/newLikes', json.dumps(payload),
                      headers={'X-API-KEY': get_api_key()})
    if r.status_code == 200:
        # self.logger.info(r.status_code)
        # self.logger.info(r.json())
        return r.json()
    else:
        click.echo('There was a problem polling the latest likes. Have you claimed your email address?')
        pprint(r.status_code)
        pprint(r.json())
        pprint(config)
        exit(1)
