import os
import requests
from celery.task import task
# from celeryconfig import app

## Run imagenet
@task(async=True)
def count_words_at_url(url):
	print(url)
	resp = requests.get(url)
	print('count_words_at_url')
	print(resp);
	return len(resp.text.split())
