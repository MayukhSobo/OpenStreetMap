import xml.etree.cElementTree as ET
from abc import ABC, abstractmethod
import os


class ParserXML(ABC):
	def __init__(self, osmFile, events=('start', 'end')):
		if osmFile.split('.')[-1].lower() != 'osm':
			raise ValueError('Error in OSM file')
		self.source = osmFile
		self._context = iter(ET.iterparse(self.source, events=events))
		self._check_root()

	@property
	def root(self):
		_, root = next(self._context)
		return root

	@property
	def context(self):
		return self._context

	def _check_root(self):
		if self.root.tag.lower() != 'osm':
			raise ValueError('OpenStreetDataMap Error')

	def _get_element(self, tags):
		for event, elem in self.context:
			if event == 'end' and elem.tag in self.tags:
				yield elem
				self.root.clear()

	@abstractmethod
	def export_dataset(fraction):
		pass


class DataFramerXML(ParserXML):
	def __init__(self, osmFile, tags, **kwargs):
		super(self.__class__, self).__init__(osmFile=osmFile)
		self._parseData = ""
		self.tags = tags
		self.exportFiles = kwargs.get('files')
		self.export = kwargs.get('export')
		self.tagValidation = kwargs.get('tagValidation', False)
		self.rootPath = kwargs.get('root', '.')
		self._validate()

	def _validate(self):
		if not self.export:
			pass
		elif self.export is None and self.exportFiles is not None or self.export is not None and self.exportFiles is None:
			raise ValueError('Export value and exportFiles doesn\'t match')

		if self.tagValidation:
			allTags = set()
			print('In Progress Tag Validation. This may take some time depending on the XML file size.....')
			for event, elem in self.context:
				allTags.add(elem.tag)

			for each in self.tags:
				if each not in allTags:
					raise ValueError('Given tags are not present in XML')

	@property
	def data(self):
		self.export_dataset()
		return self._parseData

	def export_dataset(self):
		if not os.path.exists(self.rootPath):
			raise IOError('The path doesn\'t exist.')
		for exportFile, factor in self.exportFiles.items():
			if exportFile.split('.')[-1] != 'osm':
				raise ValueError('Export files must OSM type')
			print(exportFile, factor)


def main():
	p = DataFramerXML('../../gurugram.osm', tags=('node', 'way', 'relation'), files={'test.osm': 10})
	# p.parse(factor=10000)
	p.data


if __name__ == '__main__':
	main()
