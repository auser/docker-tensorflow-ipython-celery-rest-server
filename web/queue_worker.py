import os
from redis import Redis
from rq import Queue
from rq.job import Job

# def get_job(job_id, conn=False):
# 	if not conn:
# 		conn = get_connection()

# 	return Job.fetch(job_id, connection=conn)

def get_connection():
	return Redis(
		host=os.environ.get('REDIS_PORT_6379_TCP_ADDR', '172.17.0.2'),
		port=os.environ.get('REDIS_PORT_6379_TCP_PORT', '6379'),
		db=os.environ.get('WORKER_DB', 0)
	)

def get_queue(name):
	conn = get_connection()
	if not name:
		name = 'jobs'
	return Queue(name, connection=conn)