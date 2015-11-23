import os
from celery import Celery

# print(os.environ)

redis = {
	'host': os.environ.get('REDIS_PORT_6379_TCP_ADDR', '172.17.0.2'),
	'port': os.environ.get('REDIS_PORT_6379_TCP_PORT', '6379'),
	'db': os.environ.get('WORKER_DB', '0')
}

rabbit = {
	'host': os.environ.get('RABBITMQ_PORT_5672_TCP_ADDR', '172.17.0.3'),
	'port': os.environ.get('RABBITMQ_PORT_5672_TCP_PORT', '5672'),
}

redis_backend = 'redis://' + redis.get('host') + ':' + redis.get('port') + '/' + redis.get('db')
rabbit_backend = 'amqp://' + rabbit.get('host') + ':' + rabbit.get('port') + '//'

CELERY_IMPORTS=("count",)

BROKER_URL = rabbit_backend
CELERY_RESULT_BACKEND = redis_backend

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_TIMEZONE = 'US/Los Angeles'
CELERY_ENABLE_UTC = True