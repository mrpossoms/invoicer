
#!/usr/bin/env python
from kontrack.job import Job
from kontrack.repo import Repo

import kontrack.invoicer as invoicer
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

		job.sessions().start()

		print(f'Started session for job "{args.name}"')
	elif args.command == 'stop':
		job = Job(args.name)
		job.sessions().stop(message=args.message)
		print(f'Stopped session for job "{args.name}"')
	elif args.command == 'invoice':
		job = Job(args.name)
		invoicer.start(job)

def main():
	parser = argparse.ArgumentParser(prog='kontrack')
	subparsers = parser.add_subparsers(dest='command')

	job_parser = subparsers.add_parser('job')
	job_parser.add_argument('name', type=str)
	job_parser.add_argument('command', choices=['start', 'stop', 'invoice'])
	job_parser.add_argument('--message', type=str, default=None)
	job_parser.set_defaults(func=job)

	args = parser.parse_args()
	
	# AttributeError: 'Namespace' object has no attribute 'func'
	# means that the subparser was not called, probably because of
	# a missing sub command
	args.func(args)

if __name__ == "__main__":
	main()