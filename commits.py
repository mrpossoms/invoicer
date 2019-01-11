import os
import datetime
import workweek
from subprocess import Popen, PIPE, STDOUT

class commit:
	def __init__(self, day, repo, message):
		self.day = day
		self.repo = repo 
		self.message = message

def commits(repo_path, start, stop):
	os.chdir(repo_path)
	commits = []

	cmd = 'git log'
	p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

	commit_texts = p.stdout.read().split('commit ')

	def key_value(line):
		parts = line.split(': ')
		return parts[0], parts[1]
	
	for commit_text in commit_texts:
		parts = commit_text.split('\n\n    ')
		if len(parts) < 2: continue	
		print(parts)

		key_lines = parts[0]
		msg       = parts[1]
		kvps      = {}

		for key_line in key_lines.split('\n'):
			print('"' + key_line + '"')
			key, value = key_value(key_line)
			kvps[key] = value			

		
		for key in kvps:
			print(key + '->' + kvps[key])

		print('=>' + msg)
		print('----')
