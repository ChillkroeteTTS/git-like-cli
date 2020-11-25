import json
import os

import click
from git import Repo

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


@click.command()
def like():
    config = read_config()
    repo = get_repo()
    for l in repo.blame('head', 'codelike.py'):
        click.echo(l[0].author)
        click.echo(l[1])


def get_repo():
    return Repo(os.getcwd())


if __name__ == '__main__':
    like()
