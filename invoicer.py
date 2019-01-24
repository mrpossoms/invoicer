#!/usr/bin/python3

from flask import *
import datetime
from workweek import workweek
from commits import commits


app = Flask(__name__)


def date_str(dt):
    return '%d-%d-%d' % (dt.month, dt.day, dt.year)


def total_time(work_days):
    total = 0
    for _, hours, _ in work_days:
        total += hours

    return total


def week_start_end(start):
    now = datetime.datetime.now()

    if start:
        now = datetime.datetime.strptime(start, "%Y-%m-%d")

    day = now.weekday() + 1

    start = now + datetime.timedelta(days=-day)
    end = now + datetime.timedelta(days=7 - day)

    return start, end


def get_commits(start, end, repo_paths):
    commit_table = {}

    for repo_path in repo_paths:
        if len(repo_path) == 0: continue

        for commit in commits(repo_path.rstrip(), start, end):
            if commit.date in commit_table:
                commit_table[commit.date] += [commit]
            else:
                commit_table[commit.date] = [commit]

    return commit_table


@app.route('/')
def home():
	now = datetime.datetime.now()
	return render_template('invoicer.html', start_date="{}-{:02d}-{:02d}".format(now.year, now.month, now.day))


@app.route('/week/')
def week():
    week_date = request.args.get('date')
    author    = request.args.get('author')
    repos_str = request.args.get('repos')
    repos = repos_str.split('\n')

    start, end = week_start_end(week_date)

    work, rate = workweek(start, end)
    commits = get_commits(start, end, repos)
    days = []

    for key in work:
        commit_messages = ''

        if key not in commits: continue

        for commit in commits[key]:
            if author in commit.author:
                commit_messages += commit.message + '. '

        days += [(date_str(key), round(work[key], 1), commit_messages)]

    days.sort()

    now = datetime.datetime.now()
    week = { 
            'work_days': days,
            'week_end': date_str(end),
            'now': date_str(datetime.datetime.now()),
            'total': round(total_time(days),1),
            'rate': rate,
            }

    return render_template('invoice.html', week=week)


app.run(host='0.0.0.0')
url_for('static', filename='bootstrap.min.css')
