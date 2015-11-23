from rq import Queue
from queue.queue_worker import get_queue, count_words_at_url

q = get_queue('jobs')

if __name__ == '__main__':
	result = q.enqueue(count_words_at_url, 'http://yahoo.com')
	print(result.id)