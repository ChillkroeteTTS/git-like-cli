import logging
import platform
from datetime import datetime
import time
from os.path import expanduser

from dateutil.tz import tzlocal, tzoffset

from service import Service

from gitlike.config import read_config, write_config
from gitlike.shared import  get_likes


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
        path = expanduser('~') + '/.gitlike.log'
        self.logger.addHandler(logging.FileHandler(path))
        self.logger.setLevel(logging.INFO)
        config = read_config()

        if 'lastChecked' in config.keys():
            self.lastChecked = config['lastChecked']
        else:
            self.lastChecked = get_current_utc_iso()

    def poll_new_likes(self):
        newLastChecked = get_current_utc_iso()
        get_likes(self.lastChecked)
        self.lastChecked = newLastChecked
        write_config({'lastChecked': newLastChecked})

    def run(self):
        while not self.got_sigterm():
            # self.logger.info("I'm working...")
            sleep_time_s = 60
            time.sleep(sleep_time_s)

            likes = self.poll_new_likes()

            if len(likes) > 0:
                # self.logger.info('new likes found!!!')
                for like in likes:
                    notify(like)
            else:
                # self.logger.info('no new likes found')
                pass


def handle_service(cmd):
    import sys
    service = CodelikeService('codelike', pid_dir='/tmp')
    if cmd == 'start':
        path = expanduser('~') + '/.gitlike.log'
        print('Logging: ', path)
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

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        sys.exit('Syntax: %s COMMAND' % sys.argv[0])

    cmd = sys.argv[1].lower()
    handle_service(cmd)
