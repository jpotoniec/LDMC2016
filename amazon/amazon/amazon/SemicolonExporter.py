from scrapy.contrib.exporter import CsvItemExporter
import csv

class SemicolonExporter(CsvItemExporter):
	def __init__(self, file, *args, **kwargs):
		CsvItemExporter.__init__(self, file, include_headers_line=True, delimiter=';', quoting=csv.QUOTE_ALL)
#		super(CsvItemExporter, self).__init__(file, delimiter=';', quoting=csv.QUOTE_ALL)
