#!/usr/bin/python3

from flask import *
import datetime
from workweek import workweek

app = Flask(__name__)


def date_str(dt):
    return '%d-%d-%d' % (dt.month, dt.day, dt.year)


def total_time(work_days):
    total = 0
    for _, hours in work_days:
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

@app.route('/')
def home():
	now = datetime.datetime.now()
	return render_template('invoicer.html', start_date="{}-{:02d}-{:02d}".format(now.year, now.month, now.day))

@app.route('/week/')
def week():
    week_date = request.args.get('date')
    author    = request.args.get('author')
    repos_str = request.args.get('repos')
    
    start, end = week_start_end(week_date)

    work = workweek(start, end)
    days = []

    for key in work:
        days += [(date_str(key), round(work[key], 1))]

    now = datetime.datetime.now()
    week = { 
            'work_days': days,
            'week_end': date_str(end),
            'now': date_str(datetime.datetime.now()),
            'total': total_time(days)
            }

    return render_template('invoice.html', week=week)


app.run(host='0.0.0.0')
url_for('static', filename='bootstrap.min.css')
