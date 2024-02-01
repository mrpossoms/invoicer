import os
import subprocess
from pathlib import Path
from kontrack.config import name

class Repo:
	@property
	def path(self):
		return Path.home() / Path(f'.{name()}')
	

	def __init__(self):
		if self.path.exists():
			if len(self.remotes()) > 0:
				self.pull()
		else:
			try:
				print(f'.{name()} repo missing, lets try to clone an existing one')
				username = input('Github username: ')
				self.clone(username)
			except:
				print(f'Error: cloning .{name()} repo failed, creating one instead')
				self.make()

	def make(self):
		self.path.mkdir(parents=True, exist_ok=True)

		failure = os.system(f'git init {self.path}')

		if failure > 0:
			raise Exception(f'Error: initializing .{name()} repo failed')

	def remotes(self) -> list:
		os.chdir(self.path)
		result = subprocess.run(['git', 'remote', '-v'], capture_output=True)
		if result.returncode > 0:
			raise Exception(f'Error: getting remotes from .{name()} repo failed')

		stdout = str(result.stdout, 'utf8')

		if len(stdout) == 0:
			return []

		return stdout.split('\n')

	def clone(self, username:str):
		if len(username) == 0:
			raise Exception('Error: username not provided')

		failure = os.system(f'git clone git@github.com:{username}/.{name()}.git {self.path}')
		if failure > 0:
			raise Exception(f'Error: cloning .{name()} repo failed, creating one instead')

	def pull(self):
		print(f'cd {self.path}; git pull')
		failure = os.system(f'cd {self.path}; git pull')
		if failure > 0:
			print('Error: pulling tracker git repo failed. Try pulling manually')
			


if __name__ == '__main__':
	ok = True
	try:
		Repo()
	except:
		ok = False

	assert ok == True, 'Repo creation failed'
