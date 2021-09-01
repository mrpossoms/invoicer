import os
import datetime


def work(start, end):
    home = os.path.expanduser('~') + '/'

    days = {}
    rate = 0

    with open(home + '.tracker/rate') as file:
        line = file.readline()
        rate = float(line)

    with open(home + '.tracker/sessions') as file:
        while True:
            line = None

            try:
                line = file.readline()
            except:
                break

            if line is None or len(line) <= 0:
                break

            timestamp, hours = line.split(' ')[0:2]
            timestamp = int(timestamp)
            hours = float(hours)

            day = datetime.datetime.fromtimestamp(timestamp)

            if day < start:
                continue

            if day > end:
                break

            day = datetime.datetime(
                year=day.year,
                month=day.month,
                day=day.day
            )

            if day not in days:
                days[day] = hours
            else:
                days[day] += hours

    return days, rate
