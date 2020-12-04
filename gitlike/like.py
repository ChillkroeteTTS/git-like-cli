import json
import os

import click
import requests

from gitlike.git_wrapper import git_blame

from gitlike.shared import get_repo, get_current_git_user, get_api_key


def get_git_rel_path(rel_file_path):
    git_dir = get_repo().working_dir
    abs_file_path = os.path.abspath(rel_file_path)
    common = os.path.commonpath([git_dir, abs_file_path])
    git_dir_rel_path = os.path.relpath(abs_file_path, start=common)
    return git_dir_rel_path


def like_file(file, from_line, to_line):
    repo = get_repo()
    blame = git_blame(file)
    from_l_int = int(from_line)
    to_l_int = int(to_line)
    selected_blames = blame[from_l_int - 1:to_l_int - 1] if from_line != to_line else blame[from_l_int - 1]
    authors = [c['author'] for c in selected_blames]
    emails = [c['email'] for c in selected_blames]
    revs = [c['rev'] for c in selected_blames]


    working_commits = [l for l in selected_blames if l['rev'] == '0000000000000000000000000000000000000000']
    if len(working_commits) > 0:
        # lines in working state where liked
        lNo = working_commits[0]['lineNo']
        l = working_commits[0]['line']
        click.echo(f"Please only like committed lines. You tried to like recent changes in line {lNo}: {l}")
    else:
        # committed lines where liked
        project = next(repo.remote('origin').urls)
        git_rel_file_path = get_git_rel_path(file)
        like = {
            'from_l': from_l_int,
            'to_l': to_l_int,
            'author': authors[0],
            'by': get_current_git_user(),
            'email': emails[0],
            'file': git_rel_file_path,
            'project': project,
            'commit_rev': revs[0]
        }
        # print(like)
        res = requests.post('https://1nvgpilww4.execute-api.eu-central-1.amazonaws.com/dev/like',
                            json.dumps(like),
                            headers={'X-API-KEY': get_api_key()})

        if res.status_code == 200:
            click.echo(f'''\u001b[32mLiked line {from_l_int} to {to_l_int} in {git_rel_file_path} @ {project}\u001b[37m''')
        else:
            click.echo(f'''\u001b[31mUps... Something went wrong. Sry for that.\u001b[37m''')
        # for c, l in flattened_blame:
        #     click.echo(c.author.email)
        #     click.echo(c.author + ': ' + l)
