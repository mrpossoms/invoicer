from pathlib import Path
from kontrack.repo import Repo
from typing import Tuple, List
import time
import csv

class Job:
	class Sessions:
		def __init__(self, job):
			self._job = job
			self._csv_path = self._job._path / Path('sessions.csv')

			if not self._csv_path.exists():
				self._csv_path.touch()

		@property
		def current_session_path(self):
			return self._job._path / Path('current')

		def current_session(self) -> Tuple[int, Path]:
			if not self.current_session_path.exists():
				return None

			with open(self.current_session_path, 'r') as file:
				session = file.read()

			start_time, start_cwd = session.split(',')

			return (int(start_time), Path(start_cwd))

		def start(self) -> int:
			"""
			Starts a new work session, and records it in a file at the path
			~/.kontrack/jobs/{job}/current. It stores the start time and the
			current working directory, which is used to scrape commit info
			when an invoice is generated.
			
			:raises     Exception:  If a current file already exists
			"""
			if self.current_session_path.exists():
				raise Exception(f'Error: session already in progress for job')

			start_time = int(time.time())
			self.current_session_path.write_text(f'{str(start_time)},{Path.cwd()}')
			return start_time

		def stop(self, message:str='') -> int:
			if not self.current_session_path.exists():
				raise Exception(f'Error: no session in progress for job')

			if message is None:
				message = ''

			start_time, start_cwd = self.current_session()
			end_time = int(time.time())

			with open(self._csv_path, 'a') as file:
				file.write(f'{start_time},{end_time},{start_cwd},{message}\n')

			self.current_session_path.unlink()

			return end_time

		def select(self, start_timestamp:int, end_timestamp:int) -> List[List]:
			"""
			Selects all sessions between start_timestamp and end_timestamp
			"""
			with open(self._csv_path, 'r') as file:
				reader = csv.reader(file)
				rows = list(reader)

				return [row for row in rows if int(row[0]) >= start_timestamp and int(row[1]) <= end_timestamp]

	def __init__(self, 
		name:str, 
		hourly_rate:float=None):

		self._repo = Repo()
		self._path = self._repo.path / Path('jobs') / Path(name)

		if hourly_rate is not None:
			if self._path.exists():
				raise Exception(f'Error: job {name} already exists')

			self._path.mkdir(parents=True, exist_ok=True)
			(self._path / Path('hourly_rate')).write_text(str(hourly_rate))
		else:
			if not self._path.exists():
				raise Exception(f'Error: job {name} does not exist')

	@property
	def hourly_rate(self) -> float:
		return float((self._path / Path('hourly_rate')).read_text())

	@property
	def sessions(self) -> Sessions:
		return Job.Sessions(self)


if __name__ == '__main__':
	import shutil
	import os
	# try to access a job that doesn't exist
	ok = False
	try:
		Job('test')
	except:
		ok = True
	assert(ok)
	os.system('rm -rf ~/.kontrack/jobs/test')

	# create a job
	# import pdb; pdb.set_trace()
	job = Job('test', 100)
	assert(job.hourly_rate == 100)
	
	# ensure a session is recorded correctly
	cwd = Path.cwd()
	start = job.sessions.start()
	end = job.sessions.stop()
	with open(job.sessions._csv_path, 'r') as file:
		lines = file.readlines()
		assert(lines[0] == f'{start},{end},{cwd}\n')

	# ensure sessions can be queried for a time range
	assert(len(job.sessions.select(start-1, end+1)) == 1)
	assert(len(job.sessions.select(end+1, end+2)) == 0)

	os.system('rm -rf ~/.kontrack/jobs/test')