#!/usr/bin/env python

import os
import sys
from rq import Queue, Connection, Worker
from redis import Redis

# Relative imports
sys.path.append('./queue')
from queue_worker import get_connection

redis = Redis(
		os.environ.get('REDIS_PORT_6379_TCP_ADDR', '172.17.0.2'),
		os.environ.get('REDIS_1_PORT_6379_TCP_PORT', '6379'),
		db=os.environ.get('WORKER_DB', 0)
	)

listen = os.environ.get('WORKER_QUEUES', 'jobs').split(',')

if __name__ == '__main__':
    with Connection(redis):
        worker = Worker(map(Queue, listen))
        worker.work()