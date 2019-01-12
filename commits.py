import os
import datetime
import workweek
import re
from subprocess import Popen, PIPE, STDOUT


class Commit:
    def __init__(self, repo, keys, msg):
        self.repo = repo
        self.message = msg

        self.author = keys['Author']
        _, month, day, time, year, tmz = keys['Date'].split(' ')

        months = {
            'Jan': 1,
            'Feb': 2,
            'Mar': 3,
            'Apr': 4,
            'May': 5,
            'June': 6,
            'July': 7,
            'Aug': 8,
            'Sept': 9,
            'Oct': 10,
            'Nov': 11,
            'Dec': 12
        }
        year = int(year)
        month = months[month]
        day = int(day)
        self.date = datetime.datetime(year, month, day)

    def __str__(self):
        return 'Date: {}\nAuthor: {}\nMessage: {}\n'.format(str(self.date), self.author, self.message)


def commits(repo_path, start, stop):
    os.chdir(repo_path)
    cmd = 'git log --after={}-{}-{} --before={}-{}-{}'.format(start.year, start.month, start.day, stop.year, stop.month, stop.day + 1)
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    commit_texts = re.split('commit ([0-9]|[a-z])*\n', str(p.stdout.read(), 'utf-8'))

    def key_value(line):
        parts = line.split(': ')
        return parts[0], parts[1]

    commits = []
    for commit_text in commit_texts:
        parts = commit_text.split('\n\n    ')
        if len(parts) < 2: continue

        key_lines = parts[0]
        msg = parts[1].lstrip().rstrip()
        kvps = {}

        for key_line in key_lines.split('\n'):
            key, value = key_value(key_line)
            if key is not None:
                kvps[key] = value.lstrip().rstrip()

        commits.append(Commit(repo_path, kvps, msg))

    return commits
