import os
import datetime
import workweek
import re
from subprocess import Popen, PIPE, STDOUT

class commit:
	def __init__(self, repo, keys, msg):
		self.repo = repo
		self.message = msg

		self.author = keys['Author']
		_, month, day, time, year, tmz = keys['Date'].split(' ')

		months = {
			'Jan': 1,
			'Feb': 2,
			'Mar': 3,
			'Apr': 4,
			'May': 5,
			'June': 6,
			'July': 7,
			'Aug': 8,
			'Sept': 9,
			'Oct': 10,
			'Nov': 11,
			'Dec': 12 
		}
		year = int(year)
		month = months[month]
		day = int(day)
		self.date = datetime.datetime(year, month, day)

def commits(repo_path, start, stop):
	os.chdir(repo_path)
	commits = []

	cmd = 'git log'
	p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

	commit_texts = re.split('commit ([0-9]|[a-z])*\n', p.stdout.read())

	def key_value(line):
		parts = line.split(': ')
		if len(parts) != 2: return None, None
		return parts[0], parts[1]
	
	for commit_text in commit_texts:
		parts = commit_text.split('\n\n    ')
		if len(parts) < 2: continue	

		key_lines = parts[0]
		msg       = parts[1].lstrip().rstrip()
		kvps      = {}

		for key_line in key_lines.split('\n'):
			key, value = key_value(key_line)
			if key != None: kvps[key] = value.lstrip().rstrip()
		
		for key in kvps:
			print(key + '->' + kvps[key])

		print('=>' + msg)
		print('----')

		c = Commit(repo_path, kvps, msg)