
import scrapy
from pprint import pprint
import re
import urllib
import os.path

class WikipediaSpider(scrapy.Spider):
	name = 'WikipediaScraper'
#	start_urls = ['https://en.wikipedia.org/w/index.php?title=The_Drug_in_Me_Is_You&action=edit']
	file_names = {}

	def start_requests(self):
		with open('../base.txt') as f:
			for uri in f:
				uri = uri.strip()
				name = uri
				name = name.replace('http://dbpedia.org/resource/', '')
				fn = "markdown/"+re.sub(r'\W', '_', name)+".txt"
				url = 'https://en.wikipedia.org/w/index.php?title={}&action=edit'.format(urllib.quote(name))
				if not os.path.exists(fn):
					self.file_names[url] = fn
					print(fn)
					yield scrapy.Request(url, self.parse)

	def parse(self, response):
		fn = self.file_names[response.url]
		print("{} -> {}".format(response.url, fn))
		for text in response.css('#wpTextbox1').extract():
			with open(fn, 'wt') as f:
				f.write(text.encode('UTF-8'))
