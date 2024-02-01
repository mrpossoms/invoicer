from pathlib import Path
from kontrack.repo import Repo
from typing import Tuple, List
from kontrack.commits import commits, Commit
from datetime import datetime
import time
import csv
import os

# TODO: figure out how to nest session inside of job for a more semantically meaningful type name
class Session:
	def __init__(self, start_time:int, end_time:int, cwd:Path, message:str=''):
		self._start_time = start_time
		self._end_time = end_time
		self._cwd = cwd
		self._message = message

	@property
	def hours(self) -> float:
		return (self._end_time - self._start_time) / 3600.0

	@property
	def commits(self) -> List[Commit]:
		"""
		Scrapes commit messages from the git repo at the cwd
		"""
		return commits(os.path.expanduser(self._cwd), self.start_date, self.end_date)

	@property
	def message(self) -> str:
		return self._message

	@property
	def start_date(self) -> datetime:
		return datetime.fromtimestamp(self._start_time)

	@property
	def end_date(self) -> datetime:
		return datetime.fromtimestamp(self._end_time)

class Job:


	class Sessions:
		def __init__(self, job, start_time:int=None, end_time:int=None):
			self._job = job
			self._csv_path = self._job._path / Path('sessions.csv')

			self._start_time = start_time
			self._end_time = end_time

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

		def select(self) -> List[Session]:
			"""
			Selects all sessions between start_timestamp and end_timestamp
			"""
			with open(self._csv_path, 'r') as file:
				reader = csv.reader(file)
				rows = list(reader)

				sessions = []

				for row in rows:
					sess_start, sess_end, cwd, message = int(row[0]), int(row[1]), row[2], row[3]

					if sess_start < self._start_time or sess_end > self._end_time:
						continue

					sessions.append(Session(sess_start, sess_end, cwd, message=message))

				return sessions


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

	def sessions(self, start_time:int=None, end_time:int=None) -> Sessions:
		return Job.Sessions(self, start_time=start_time, end_time=end_time)


	@staticmethod
	def jobs() -> List[str]:
		"""
		Returns a list of all jobs
		"""
		repo = Repo()
		jobs_path = repo.path / Path('jobs')
		return [job.name for job in jobs_path.iterdir() if job.is_dir()]

if __name__ == '__main__':
	import shutil
	import os

	os.system('rm -rf ~/.kontrack/jobs/test')

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
	start = job.sessions().start()
	end = job.sessions().stop()
	with open(job.sessions()._csv_path, 'r') as file:
		lines = file.readlines()
		assert(lines[0] == f'{start},{end},{cwd},\n')

	# ensure sessions can be queried for a time range
	assert(len(job.sessions(start-1, end+1).select()) == 1)
	assert(len(job.sessions(end+1, end+2).select()) == 0)

	os.system('rm -rf ~/.kontrack/jobs/test')