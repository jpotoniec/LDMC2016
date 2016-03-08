# -*- coding: utf-8 -*-
import scrapy
import scrapy
from pprint import pprint
import re
import urllib
import os.path
from amazon.items import AmazonItem


class AmazonSpider(scrapy.Spider):
	name = 'AmazonSpider'
	start_urls = ['http://amazon.com']

	#albums = {'http://dbpedia.org/resource/In_Rape_Fantasy_and_Terror_Sex_We_Trust': ('Joan of Arc', 'In Rape Fantasy And Terror Sex We Trust')}
	albums = {}

	def __init__(self):
		scrapy.Spider.__init__(self)
		for fn in ['../../trainingDataset.tsv', '../../testDataset.tsv']:
			with open(fn, 'rt') as f:
				for line in f:
					line = line.strip().split('\t')
					(_, uri, album, author) = line[0:4]
					self.albums[uri] = (author, album)

	def album_site(self, response):
		rating = None
		nusers = None
		for element in response.css('#avgRating span a span::text').extract():
			element = element.strip()
			m = re.match('^([0-9.]+)\s+', element)
			if m is not None:
				try:
					rating = float(m.group(1))
				except:
					pass
		for element in response.xpath(r'//*[@id="summaryStars"]//a/child::text()').extract():
			element = element.strip()
			if len(element)>0:
				try:
					nusers = int(element)
				except:
					pass
		yield AmazonItem({'uri': response.meta['uri'], 'amazon_rating': rating, 'amazon_nusers': nusers})

	def search_result(self, response):
		for url in response.css('#result_0 a.s-access-detail-page::attr("href")').extract():
			yield scrapy.Request(url, self.album_site, meta={'uri': response.meta['uri']})

	def parse(self, response):
		for uri,(author, album) in self.albums.items():
			yield scrapy.FormRequest.from_response(response, formname='site-search', formdata={'url': 'search-alias=popular', 'field-keywords': author+': '+album}, callback=self.search_result, meta={'uri': uri})
