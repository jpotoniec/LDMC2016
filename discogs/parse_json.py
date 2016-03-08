#!/usr/bin/env python3

import json
import re
import os.path

with open('../base.txt', 'rt') as f:
	print('"URI";"discogs_have";"discogs_want"')
	for uri in f:
		uri = uri.strip()
		name = uri.replace('http://dbpedia.org/resource/', '')
		fn = "json/"+re.sub(r'\W', '_', name)+".json"
		if not os.path.exists(fn):
			continue
		with open(fn, 'rt') as g:
			data = json.load(g)
			have = 0
			want = 0
			for item in data['results']:
				have += int(item['community']['have'])
				want += int(item['community']['want'])
			print('"{}";"{}";"{}"'.format(uri, have, want))

