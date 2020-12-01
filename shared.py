import re
from os.path import expanduser

def get_api_key():
    return open('./apiKey').read().replace('\n', '')


def get_current_git_user():
    with open(expanduser("~") + '/.gitconfig', 'r') as f:
        lines = [l for l in f.readlines() if 'email' in l]

    if (len(lines) > 0):
        email = re.search('=\s*(.*)$', lines[0]).group(1)
        return email
    else:
        print('Could not find gitconfig with email', lines)

