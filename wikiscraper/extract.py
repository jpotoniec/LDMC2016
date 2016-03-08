#!/usr/bin/env python3

import glob
import re


#| rev1 = [[AllMusic]]
#| rev1Score = {{Rating|5|5}}&lt;ref name="AllMusic"&gt;{{cite web |url=http://www.allmusic.com/album/whatever-people-say-i-am-thats-what-im-not-mw0000703071 |title=Whatever People Say I Am, That's What I'm Not – Arctic Monkeys |publisher=[[AllMusic]] |accessdate=19 February 2014 |last=Erlewine |first=Stephen Thomas |authorlink=Stephen Thomas Erlewine}}&lt;/ref&gt;

re_rev = re.compile(r'rev(\d+)\s*=([^|]*)',re.IGNORECASE)
re_revScore = re.compile(r'\|\s*rev(\d+)Score\s*=(.*)$',re.IGNORECASE)

#{{Rating|3|5}}
re_rating = re.compile(r'{{\s*Rating\s*\|\s*([0-9.]+)\s*\|\s*([0-9.]+)', re.IGNORECASE)
#(8.3/10)&lt;ref name="UG"/&gt;
re_parenth = re.compile(r'\(([0-9.]+)/([0-9.]+)\)', re.IGNORECASE)
#1.5/10 [http://www.pitchforkmedia.com/article/record_review/49081-robotique-majestique link]
re_start = re.compile(r'^([0-9.]+)\s*/\s*([0-9.]+)', re.IGNORECASE)
#[[AbsolutePunk]] -> (86%)&lt;ref name="AP"/&gt;
re_percent_parenth = re.compile(r'\(([0-9.]{1,3})%\)', re.IGNORECASE)
#rev2Score=86% [http://www.cokemachineglow.com/record_review/4789/circulatorysystem-signalmorning-2009 link]
re_percent_begin = re.compile(r'^([0-9.]{1,3})%', re.IGNORECASE)
#[[Pitchfork Media]] -> (7.9)&lt;ref&gt;[http://pitchfork.com/reviews/albums/1633-party-music/ Pitchfork Media review]&lt;/ref&gt;
re_single = re.compile(r'(?:^(?:\'{2,4})?|\()([0-9.]{1,2})')
#''[[Entertainment Weekly]]'' -> A–&lt;ref name="EW"&gt;{{cite journal |url=http://www.ew.com/article/2006/02/20/whatever-people-say-i-am-thats-what-im-not |title=Whatever People Say I Am, That's What I'm Not |work=[[Entertainment Weekly]] |date=20 February 2006 |accessdate=23 April 2012 |last=Browne |first=David |authorlink=David Browne}}&lt;/ref&gt;
#[[Robert Christgau]] -> (A)&lt;ref&gt;[http://www.robertchristgau.com/get_artist.php?id=1404&amp;name=The+Coup Robert Christgau review]&lt;/ref&gt;
#'''A–'''&lt;ref name="Stylus"&gt;{{cite web |first=Nick |last=Mims |title=Joseph Arthur - Our Shadows Will Remain - Review |url=http://www.stylusmagazine.com/reviews/joseph-arthur/our-shadows-will-remain.htm |publisher=''[[Stylus Magazine]]'' |date=20 January 2005 |accessdate=23 July 2010
re_letter = re.compile(r'(?:^(?:\'{2,3})?|\()([A-F][+-]?)')
#''[[Billboard (magazine) -> (favorable)&lt;ref&gt;{{Wayback |date=20080503212819 |url=http://www.billboard.com/bbcom/content_display/reviews/albums/e3i9fd76a66aebe6d4c64e17bb437a80f27 |title=Billboard review}}&lt;/ref&gt;
#''[[The Boston Globe]]'' -> (positive)&lt;ref&gt;[http://www.boston.com/ae/music/cd_reviews/articles/2008/05/06/somebody_got_his_heart_broken/ The Boston Globe review]{{subscription required}}&lt;/ref&gt;
#''[[The New York Times]]'' -> (average)&lt;ref&gt;[http://www.nytimes.com/2008/05/05/arts/music/05choi.html?_r=0 The New York Times review]&lt;/ref&gt;
#[[BBC Music]] -> negative&lt;ref&gt;http://www.bbc.co.uk/music/reviews/2h28&lt;/ref&gt;
#motor.de -> (unfavourable)&lt;ref name=motor/&gt;
#''The Brock Press'' -> (neutral)&lt;ref name=brock/&gt;
re_word = re.compile(r'(?:^|\()(?:\'{2,3})?((?:very\s+|highly\s+|fairly\s+|generally\s+|somewhat\s+)?(?:favou?rable|ambivalent|unfavou?rable|neutral|positive?|average|negative|mixed))', re.IGNORECASE)
#[[Robert Christgau]] -> {{Rating-Christgau|A-}}&lt;ref name="Christgau review"/&gt;
re_christgau = re.compile(r'{{\s*Rating-Christgau\s*\|\s*([^\|]*?)\s*(?:\|.*)?}}', re.IGNORECASE)

re_good = re.compile('(favou?rable|positive?)')
re_neutral = re.compile('(neutral|average|mixed|ambivalent)')
re_negative = re.compile('(unfavou?rable|negative)')

def normalize(score):
	if not isinstance(score, str):
		return score
	score = score.lower()
	if len(score) <= 2:
		m = {'a': .9, 'b': .8, 'c': .7, 'd': .6, 'e': .5, 'f': 0}
		val = m[score[0]]
		if len(score) == 2:
			if score[1] == '+':
				val += .05
			elif score[1] == '-':
				val -= .05
			else:
				raise Exception("Can not normalize: {}".format(score))
		return val
	# https://en.wikipedia.org/wiki/Template:Rating-Christgau
	if score == 'hm3':
		return 1
	if score == 'hm2':
		return .8
	if score == 'hm1':
		return .6
	if score == 'neither':
		return .5
	if score == 'cut':
		return .2
	if score == 'dud':
		return 0
	if re_good.search(score) is not None:
		return 1
	if re_neutral.search(score) is not None:
		return .5
	if re_negative.search(score) is not None:
		return 0
	raise Exception("Can not normalize: {}".format(score))


def normalize_name(name):
	name = name.lower()
	name = re.sub(r'[\'\[\]]', '', name)
	name = re.sub(r'\{\{.*$', '', name)
	name = re.sub(r'\(.*$', '', name)
	name = re.sub(r'\&.*$', '', name)
	name = re.sub(r'\..*$', '', name)
	name = re.sub(r'http.*$', '', name)
	name = re.sub(r'\W', '', name)
	name = re.sub("(maga)?zine", '', name)
	name = re.sub("the", '', name)
	name = "".join(name.split()[:2])
	begins = ["bbc", "yahoo", "times", "virgin", "ultimateguitar", 'villagevoice']
	for b in begins:
		if name.startswith(b):
			return b
	return name

data = {}
counter = {}
files = {}

with open('../base.txt') as f:
	for uri in f:
		uri = uri.strip()
		name = uri.replace('http://dbpedia.org/resource/', '')
		fn = "markdown/"+re.sub(r'\W', '_', name)+".txt"
		files[uri] = fn


for uri, fn in files.items():
#	print()
#	print(fn)
	names = {}
	scores = {}
	with open(fn,'rt') as f:
		for line in f:
			line = line.strip()
			m = re_rev.search(line)
			if m is not None:
				names[m.group(1)] = normalize_name(m.group(2).strip())
			m = re_revScore.search(line)
			if m is not None:
				n = m.group(1)
				score = m.group(2).strip()
				if len(score) == 0:
					continue
				m = re_rating.search(score) or re_parenth.search(score) or re_start.search(score)
				if m is not None:
					scores[n] = float(m.group(1))/float(m.group(2))
					continue
				m = re_percent_parenth.search(score) or re_percent_begin.search(score)
				if m is not None:
					scores[n] = float(m.group(1))/100
					continue
				m = re_word.search(score) or re_letter.search(score) or re_christgau.search(score)
				if m is not None:
					scores[n] = m.group(1)
					continue
				m = re_single.search(score)
				if m is not None:
					print(score)
					scores[n] = float(m.group(1))/10
					continue
				print("Can't deal with '{}'".format(score))
	data[uri]={}
	for n in names.keys() & scores.keys():
		data[uri][names[n]]=normalize(scores[n])
		if names[n] not in counter:
			counter[names[n]] = 0
		counter[names[n]] += 1

names = [n for n in counter.keys() if counter[n] >= 10]

def make_row(id, data):
	return '"'+str(id)+'";'+";".join(['"'+re.sub(r'"', '_', str(val))+'"' for val in data])

with open('reviews.csv','wt') as f:
	print(make_row('', names), file=f)
	for uri in files.keys():
		row = []
		for n in names:
			if n in data[uri]:
				row.append(data[uri][n])
			else:
				row.append('')
		print(make_row(uri, row), file=f)
		
