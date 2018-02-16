#!/usr/bin/python3

from flask import *
import datetime
from workweek import workweek

app = Flask(__name__)

def date_str(dt):
    return '%d-%d-%d' % (dt.month, dt.day, dt.year)

def wd(month, day, year, hours):
    return (date_str(datetime.datetime(year=year, month=month, day=day)), hours)

def total_time(work_days):
    total = 0
    for _, hours in work_days:
        total += hours

    return total


def week_start_end():
    now = datetime.datetime.now()
    day = now.weekday() + 1

    start = now + datetime.timedelta(days=-day)
    end = now + datetime.timedelta(days=6 - day)

    return start, end


@app.route('/')
def index():
    start, end = week_start_end()
    work = workweek(start, end)

    days = [
            wd(2, 7, 2018, 4),
            wd(2, 8, 2018, 3.5),
            wd(2, 9, 2018, 5.5)
            ]

    now = datetime.datetime.now()
    week = { 
            'work_days': days,
            'week_end': date_str(datetime.datetime(month=2, day=10, year=2018)),
            'now': date_str(datetime.datetime.now())
            }
    week['total'] = total_time(week['work_days'])

    return render_template('invoice.html', week=week)

app.run(host='0.0.0.0')
url_for('static', filename='bootstrap.min.css')
