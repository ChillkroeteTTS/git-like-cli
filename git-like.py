import functools
import json
import os

import click
import requests
from git import Repo

from config import Config, read_config, write_config, get_config_path, config_is_valid
from gitlike_service import handle_service
from shared import get_current_git_user


@click.group()
def main():
    pass



@click.command()
@click.argument('file', type=click.Path(exists=True))
@click.argument('from_line')
@click.argument('to_line')
def like(file, from_line, to_line):
    if not config_is_valid():
        exit_with_invalid_config()

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
    requests.post('https://1nvgpilww4.execute-api.eu-central-1.amazonaws.com/dev/like',
                  json.dumps(like),
                  headers={'X-API-KEY': 'GwHQ9OUXum5EilDTmGJJB4nnFSEaKBle76DvSNz7'})
    # for c, l in flattened_blame:
    #     click.echo(c.author.email)
    #     click.echo(c.author + ': ' + l)


@main.command()
@click.argument('email')
@click.option('--code', help='The access code you received via email.')
def claim(email, code):
    if code is not None:
        # validate access code
        validationRes = requests.post('https://1nvgpilww4.execute-api.eu-central-1.amazonaws.com/dev/access/validate',
                      json.dumps({'user': email, 'code': code}),
                      headers={'X-API-KEY': 'GwHQ9OUXum5EilDTmGJJB4nnFSEaKBle76DvSNz7'})
        print(validationRes.text)
        isValid = validationRes.json()['isValid']

        if isValid:
            write_config({'code': code, 'email': email})
            click.echo(
                f'''You successfully claimed {email}. Once you started the git-like dameon process you will start receiving likes!''')
        else:
            click.echo('The provided access code was invalid.')
            exit(1)
    else:
        # create access code
        requests.post('https://1nvgpilww4.execute-api.eu-central-1.amazonaws.com/dev/access',
                      json.dumps({'email': email}),
                      headers={'X-API-KEY': 'GwHQ9OUXum5EilDTmGJJB4nnFSEaKBle76DvSNz7'})
        print(f'''We send you a confirmation mail. Claim your email by using: git-like claim {email} --code [CODE]''')


@main.command()
def start():
    if not config_is_valid():
        exit_with_invalid_config()
    handle_service('start')


@main.command()
def stop():
    if not config_is_valid():
        exit_with_invalid_config()
    handle_service('start')


def exit_with_invalid_config():
    click.echo(
        'Your .gitlike config is invalid. Please check it before continuing. You can find the config under' + get_config_path())
    exit(1)


def remove_duplicates(l):
    return list(dict.fromkeys(l))


def get_repo():
    return Repo(os.getcwd())


if __name__ == '__main__':
    main()
