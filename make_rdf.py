#!/usr/bin/env python3

import csv

def print_ttl(uri, values):
	metrics = []
	for name, value in values.items():
		metrics.append('[ :name "{}"; :value "{}"^^xsd:double ]'.format(name, value))
	print("<{}> :has_metric {}.".format(uri, ", ".join(metrics)))

def process(f):
	reader = csv.reader(f, delimiter=';', quotechar='"')
	header = next(reader)
#	print(headers)
	for row in reader:
		name = None
		values = {}
		for i,val in enumerate(row):
			if header[i] in ('','URI','uri','id'):
				name = row[i]
			else:
				if len(val) > 0:
					values[header[i]] = val
		if len(values) > 0:
			print_ttl(name, values)

if __name__ == '__main__':
	print("@prefix : <https://github.com/jpotoniec/LDMC2016#> .")
	print("@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .")
	files = ['amazon/amazon/result.csv', 'discogs/discogs.csv', 'wikiscraper/reviews.csv', 'musicbrainz/ratings.csv']
	for file in files:
		with open(file, 'rt') as f:
			process(f)
