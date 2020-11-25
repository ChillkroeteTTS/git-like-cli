import json
import logging
import os
import platform
from datetime import datetime
import time

import requests
from dateutil.tz import tzlocal, tzoffset

from service import find_syslog, Service
from shared import get_current_git_user


def get_current_utc_iso():
    return datetime.now(tzlocal()).astimezone(tzoffset(None, 0)).isoformat()[:-8] + 'Z'


def notify(like):
    import os
    lines = str(like['from_l']) + '-' + str(like['to_l'])
    project = like['project'].split('/')[1]
    title = f'''Your Code in {project} was liked!'''
    msg = f'''
Project: {like['project']} - {lines}
By: {like['by']}\n
'''

    plt = platform.system()
    if plt == 'Darwin':
        command = f'''osascript -e 'display notification "{msg}" with title "{title}"  sound name "Basso.aiff"'
'''
    elif plt == 'Linux':
        command = f'''notify-send "{title}" "{msg}"
'''
    else:
        print('windows is not supported')
        return

    os.system(command)


class CodelikeService(Service):

    def __init__(self, *args, **kwargs):
        super(CodelikeService, self).__init__(*args, **kwargs)
        path = str.join('/', find_syslog().split('/')[:-1]) + '/codelike.log'
        print(path)
        self.logger.addHandler(logging.FileHandler(os.getcwd() + '/like.log'))
        self.logger.setLevel(logging.INFO)
        self.lastChecked = get_current_utc_iso()

    def poll_new_likes(self, user):
        newLastChecked = get_current_utc_iso()

        self.logger.info(self.lastChecked + ' ' + user)
        payload = {
            'user': user,
            'lastChecked': self.lastChecked
        }
        r = requests.post('https://1nvgpilww4.execute-api.eu-central-1.amazonaws.com/dev/newLikes', json.dumps(payload),
                          headers={'X-API-KEY': 'GwHQ9OUXum5EilDTmGJJB4nnFSEaKBle76DvSNz7'})
        self.lastChecked = newLastChecked
        self.logger.info(r.status_code)
        self.logger.info(r.json())
        return r.json()

    def run(self):
        while not self.got_sigterm():
            self.logger.info("I'm working...")
            time.sleep(5)
            current_user = get_current_git_user()
            likes = self.poll_new_likes(current_user)
            if len(likes) > 0:
                self.logger.info('new likes found!!!')
                for like in likes:
                    notify(like)
            else:
                self.logger.info('no new likes found')


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        sys.exit('Syntax: %s COMMAND' % sys.argv[0])

    cmd = sys.argv[1].lower()
    service = CodelikeService('codelike', pid_dir='/tmp')

    if cmd == 'start':
        service.start()
    elif cmd == 'stop':
        service.stop()
    elif cmd == 'status':
        if service.is_running():
            print("Service is running.")
        else:
            print("Service is not running.")
    else:
        sys.exit('Unknown command "%s".' % cmd)
