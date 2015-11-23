import os

bind = '0.0.0.0:8000'
workers = 3
backlog = 2048
worker_class = "sync"
debug = False
proc_name = 'gunicorn.proc'
pidfile = '/tmp/gunicorn.pid'
accesslog = '/var/log/gunicorn/debug.log'	
errorlog = '/var/log/gunicorn/error.log'
loglevel = 'info'
