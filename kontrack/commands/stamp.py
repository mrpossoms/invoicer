#!/usr/bin/env python

import sys 
import time
import datetime

print(int(time.mktime(datetime.datetime.strptime(sys.argv[1], "%d-%m-%Y").timetuple())))
