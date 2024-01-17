#!/usr/bin/env python

import os
import time
import datetime
import argparse

started = 0
now = int(time.time());
hours_worked = 0
rate = 0

home = os.path.expanduser('~/')
data_path = os.path.expanduser('~/.tracker')

parser = argparse.ArgumentParser(description='Stop tracking and record current work session')
parser.add_argument('-m', '--message', help='Comment about work session', required=False)

def commit(msg):
	return os.system('cd {}; git add sessions; git commit -m"{}"'.format(data_path, msg)) == 0

def push():
	return os.system('cd {}; git push'.format(data_path)) == 0

if __name__ == '__main__':
    args = parser.parse_args()

    try:
        session_path = home + '.tracker/current'
        with open(session_path, 'r') as file:
            started = int(file.read())
            hours_worked = float(now - started) / 3600
            print('Worked for %0.2f hrs' % hours_worked)
        os.unlink(session_path)
            
    except OSError:
        print('No tracking file found!')

    with open(home + '.tracker/sessions', 'a+') as file:
            file.write('%d,%f,%s\n' % (started, hours_worked, args.message if args.message else ''))

    with open(home + '.tracker/rate') as file:
        rate = float(file.read())
        print('Earned %0.2f' % (hours_worked * rate))

    if commit('Work finished at: {}'.format(time.ctime())):
    	push()
