import functools
import json
import os

import click
import requests
from git import Repo

from shared import get_current_git_user

CONFIG_PATH = '.codelike'


@click.group()
def main():
    click.echo('hello world')


@main.command()
def init():
    repo = get_repo()
    head = repo.head.commit.message
    click.echo('Init')
    firstOriginUrl = next(repo.remote('origin').urls)
    click.echo(firstOriginUrl)

    config: Config = {
        'name': firstOriginUrl
    }

    with open(CONFIG_PATH, 'w+') as f:
        f.write(json.dumps(config))
    click.echo('initialized ' + config['name'])


class Config(object):
    name: str


def read_config() -> Config:
    with open(CONFIG_PATH, 'r') as f:
        return json.loads(f.read())

def remove_duplicates(l):
    return list(dict.fromkeys(l))

@click.command()
@click.argument('file')
@click.argument('from_line')
@click.argument('to_line')
def like(file, from_line, to_line):
    config = read_config()
    repo = get_repo()
    blame = repo.blame('head', file, incremental=False)
    flattened_blame = functools.reduce(lambda agg, cAndLines: agg + [(cAndLines[0], l) for l in cAndLines[1]],
                                       blame,
                                       [])

    from_l_int = int(from_line)
    to_l_int = int(to_line)

    emails = remove_duplicates([c.author for c, l in flattened_blame[from_l_int:to_l_int]])
    click.echo(emails)

    like = {
        'from_l': from_l_int,
        'to_l': to_l_int,
        'author': emails[0].email,
        'by': get_current_git_user(),
        'email': emails[0].email,
        'file': file,
        'project': next(repo.remote('origin').urls)
    }
    print(like)
    requests.post('https://1nvgpilww4.execute-api.eu-central-1.amazonaws.com/dev/like', json.dumps(like),
                  headers={'X-API-KEY': 'GwHQ9OUXum5EilDTmGJJB4nnFSEaKBle76DvSNz7'})
    # for c, l in flattened_blame:
    #     click.echo(c.author.email)
    #     click.echo(c.author + ': ' + l)


def get_repo():
    return Repo(os.getcwd())


if __name__ == '__main__':
    like()
