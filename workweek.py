import os
import datetime


def workweek(start, end):
    home = os.path.expanduser('~') + '/'

    days = {}

    with open(home + '.tracker/sessions') as file:
        while True:
            line = None

            try:
                line = file.readline()
            except:
                break

            if line is None or len(line) <= 0:
                break

            timestamp, hours = line.split(' ')
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

            key = str(day)
            if key not in days:
                days[key] = hours
            else:
                days[key] += hours

    return days