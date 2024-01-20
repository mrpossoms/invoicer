
#!/usr/bin/env python
from kontrack.job import Job
from kontrack.repo import Repo

import argparse

def job(args):
	if args.command == 'start':
		job = None
		try:
			job = Job(args.name)
		except Exception as e:
			print('Could not find job, creating one')
			hourly_rate = float(input('Hourly rate: '))
			job = Job(args.name, hourly_rate)

		job.sessions.start()

		print(f'Started session for job "{args.name}"')
	elif args.command == 'stop':
		stop_par

		job = Job(args.name)
		job.sessions.stop()
		print(f'Stopped session for job "{args.name}"')
	elif args.command == 'invoice':
		job = Job(args.name)
		job.invoice()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog='kontrack')
	subparsers = parser.add_subparsers(dest='command')

	job_parser = subparsers.add_parser('job')
	job_parser.add_argument('name', type=str)
	job_parser.add_argument('command', choices=['start', 'stop', 'invoice'])
	job_parser.set_defaults(func=job)

	args = parser.parse_args()
	args.func(args)