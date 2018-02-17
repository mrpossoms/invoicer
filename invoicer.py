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


def week_start_end():
    now = datetime.datetime.now()
    day = now.weekday() + 1

    start = now + datetime.timedelta(days=-day)
    end = now + datetime.timedelta(days=7 - day)

    return start, end


@app.route('/')
def index():
    start, end = week_start_end()
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
