import requests

## Run imagenet
def count_words_at_url(url):
	print('here')
	resp = requests.get(url)
	print('count_words_at_url')
	print(resp);
	return len(resp.text.split())
