import os
import re
import sys

header_regex = '^([^\s]*) [0-9]+ ([0-9]+) ?[0-9]*\n$'


def extract_info(chunk):
    return {
        'rev': re.search(header_regex, chunk[0]).group(1),
        'author': re.search('author (.*)', chunk[1]).group(1),
        'email': re.search('author-mail <(.*)>', chunk[2]).group(1),
        'lineNo': re.search(header_regex, chunk[0]).group(2),
        'line': chunk[-1],
    }



def git_blame(file_name):
    cmd = 'git blame --line-porcelain {fname}'.format(
    fname=file_name)
    with os.popen(cmd) as process:
        blame = process.readlines()

    chunks = []
    curr_header_line = 0
    for i, l in enumerate(blame):
        if i == (len(blame) - 1):
            chunks += [blame[curr_header_line:i+1]]
        else:
            is_header = re.match(header_regex, l) is not None
            if is_header:
                if not curr_header_line == i:
                    # slice chunk out of line list
                    chunks += [blame[curr_header_line:i]]
                curr_header_line = i


    return [extract_info(chunk) for chunk in chunks]

if __name__ == '__main__':
    # debug
    print(sys.argv[1])
    chunks = git_blame(sys.argv[1])
    for chunk in chunks:
        print(chunk)
