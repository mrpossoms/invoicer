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
        net_hours = 0
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
            net_hours += hours

            day = datetime.datetime.fromtimestamp(timestamp)

            if day < start:
                continue

            if day > end:
                continue

            day = datetime.datetime(
                year=day.year,
                month=day.month,
                day=day.day
            )

            if day not in days:
                days[day] = hours
            else:
                days[day] += hours

    net_hours = 0
    for day in days:
        print('{} - {}'.format(day, days[day]))
        net_hours += days[day]
    print('net: {}'.format(net_hours))


    return days, rate
