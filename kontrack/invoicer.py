#!/usr/bin/env python

from flask import *
from datetime import datetime, timedelta
from job import Job
# import workweek
# from commits import commits


app = Flask(__name__)


def date_str(dt):
    return '%d-%d-%d' % (dt.month, dt.day, dt.year)


def total_time(work_days):
    total = 0
    for _, hours, _ in work_days:
        total += hours

    return total


def start(job):
    def week_start_end(start):
        now = datetime.now()

        if start:
            now = datetime.strptime(start, "%Y-%m-%d")

        day = now.weekday() + 1

        start = now + timedelta(days=-day)
        end = now + timedelta(days=7 - day)

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
    	now = datetime.now()
    	return render_template('invoicer.html', jobs=Job.jobs(), end_date="{}-{:02d}-{:02d}".format(now.year, now.month, now.day))


    @app.route('/week/')
    def week():
        job_name   = request.args.get('job-name')
        week_date  = request.args.get('date')
        start_date = request.args.get('start-date')
        end_date   = request.args.get('end-date')
        author     = request.args.get('author')
        repos_str  = request.args.get('repos')
        repos = repos_str.split('\n')

        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)

        if start is None and end is None:
            start, end = week_start_end(week_date)

        # TODO
        job = Job(job_name)
        work, rate = job.sessions(datetime.timestamp(start), datetime.timestamp(end)).select(), job.hourly_rate
        # commits = get_commits(start, end, repos)
        days = []

        for session in work:
            days += [(session.start_date, round(session.hours, 1), [str(c) for c in session.commits] + [session.message])]

        # for key in work:
        #     commit_messages = ''

        #     if key in commits:
        #         for commit in commits[key]:
        #             if author in commit.author:
        #                 commit_messages += commit.message + '. '

        # days += [(key, round(work[key], 1), commit_messages)]

        days.sort()

        now = datetime.now()
        week = { 
                'work_days': days,
                'start_date': date_str(start),
                'end_date': date_str(end),
                'now': date_str(datetime.now()),
                'total': round(total_time(days),1),
                'rate': rate,
                }

        return render_template('invoice.html', week=week)

    app.run(host='0.0.0.0')
    url_for('static', filename='bootstrap.min.css')
