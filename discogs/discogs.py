#!/usr/bin/env python3

import json
import urllib
import urllib.parse
import urllib.request
import re
from pprint import pprint
from discogs_token import token

def make_request(page, params):
	url = 'https://api.discogs.com/'+page+"?"+urllib.parse.urlencode(params)
	print(url)
	headers = {
		'Authorization': 'Discogs token='+token,
		'User-Agent': 'ReviewsScrapeBot (discogs@grota.be)'
	}
	r = urllib.request.Request(url, headers=headers)
	return urllib.request.urlopen(r)

for fn in ['../trainingDataset.tsv', '../testDataset.tsv']:
	with open(fn, 'rt') as f:
		f.readline()	#ignorujemy pierwszy wiersz
		for line in f:
			line = line.strip().split('\t')
			(_, uri, album, author) = line[0:4]
			print(uri)
			with make_request('/database/search', {'artist': author, 'release_title': album}) as f:
				data = f.read()
			name = uri.replace('http://dbpedia.org/resource/', '')
			fn = "json/"+re.sub(r'\W', '_', name)+".json"
			print(len(data))
			with open(fn, 'wb') as f:
				f.write(data)
