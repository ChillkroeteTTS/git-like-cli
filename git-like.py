import functools
import json
import os

import click
import requests
from git import Repo

from config import Config, read_config, write_config, get_config_path, config_is_valid
from git_wrapper import git_blame
from gitlike_service import handle_service
from shared import get_current_git_user, get_api_key


@click.group()
def main():
    pass



@main.command()
@click.argument('file', type=click.Path(exists=True))
@click.argument('from_line')
@click.argument('to_line')
def like(file, from_line, to_line):
    if not config_is_valid():
        exit_with_invalid_config()

    repo = get_repo()
    blame = git_blame(file)

    from_l_int = int(from_line)
    to_l_int = int(to_line)
    selected_blames = blame[from_l_int - 1:to_l_int - 1]

    authors = [c['author'] for c in selected_blames]
    emails = [c['email'] for c in selected_blames]
    revs = [c['rev'] for c in selected_blames]

    own_commits = [l for l in selected_blames if l['rev'] == '0000000000000000000000000000000000000000']
    if len(own_commits) > 0:
        lNo = own_commits[0]['lineNo']
        l = own_commits[0]['line']
        click.echo(f"Please only like committed lines. You tried to like recent changes in line {lNo}: {l}")
    else:
        like = {
            'from_l': from_l_int,
            'to_l': to_l_int,
            'author': authors[0],
            'by': get_current_git_user(),
            'email': emails[0],
            'file': file,
            'project': next(repo.remote('origin').urls),
            'commit_rev': revs[0]
        }
        print(like)
        requests.post('https://1nvgpilww4.execute-api.eu-central-1.amazonaws.com/dev/like',
                      json.dumps(like),
                      headers={'X-API-KEY': get_api_key()})
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
                      headers={'X-API-KEY': get_api_key()})
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
                      headers={'X-API-KEY': get_api_key()})
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
    return Repo()


if __name__ == '__main__':
    main()
