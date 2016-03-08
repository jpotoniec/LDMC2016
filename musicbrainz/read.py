#!/usr/bin/env python3

import gzip
import pickle
from rdflib import URIRef, Literal, BNode
import re

uri = 'http://www.wikidata.org/wiki/Q7353440'

def load(fn):
	data = []
	n = None
	with open('mbdump/'+fn, 'rt') as f:
		for line in f:
			row = line.rstrip('\r\n').split('\t')
			if n is None:
				n = len(row)
			else:
				assert n == len(row)
			data.append(row)
	return data

def make_dict(data, key_field):
	return {row[key_field]: row for row in data}

def normalize(text):
	if text == r'\N':
		return ''
	else:
		return text

triples = []
with gzip.open('../level1.pickled.gz') as f:
	triples = pickle.load(f)

sameas = {}
for s,p,o in triples:
	if p != URIRef('http://www.w3.org/2002/07/owl#sameAs'):
		continue
	if s not in sameas:
		sameas[s] = []
	sameas[s].append(o)
	if o not in sameas:
		sameas[o] = []
	sameas[o].append(s)


with open('../base.txt', 'rt') as f:
	uris = set([URIRef(uri.strip()) for uri in f])

wikidata={}

for uri in uris:
	if uri in sameas:
		for other in sameas[uri]:
			if str(other).startswith('http://wikidata.org/'):
				other = re.sub('^.*/([^/]+)$', r'\1', other)
				wikidata[uri] = other

print(len(uris), len(wikidata.keys()))

url_data = load('url')
release_group_url = make_dict(load('l_release_group_url'), 3)
release_group_meta = make_dict(load('release_group_meta'), 0)

with open('ratings.csv', 'wt') as f:
	print('"id";"mb_avg_rating";"mb_n_users"', file=f)
	for uri, id in wikidata.items():
		print(uri)
		for row in url_data:
			if row[2].endswith(id):
				url_key = row[0]
				release_group_key = release_group_url[url_key][2]
				rating, nusers = release_group_meta[release_group_key][5:7]
				print('"{}";"{}";"{}"'.format(uri, normalize(rating), normalize(nusers)), file=f)
				print("\tHIT")
