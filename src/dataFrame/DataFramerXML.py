import xml.etree.cElementTree as ET
from abc import ABC, abstractmethod


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

	@abstractmethod
	def parse(self):
		pass

	@abstractmethod
	def export_dataset(fraction):
		pass


class DataFramerXML(ParserXML):
	def __init__(self, osmFile, tags, **kwargs):
		super(self.__class__, self).__init__(osmFile=osmFile)
		self.tags = tags
		self.exportMaps = kwargs.get('files')
		self.export = kwargs.get('export')
		self.tagValidation = kwargs.get('tagValidation', False)
		self._validate()

	def _validate(self):
		if not self.export:
			pass
		elif self.export is None and self.exportMaps is not None or self.export is not None and self.exportMaps is None:
			raise ValueError('Export value and exportMaps doesn\'t match')

		if self.tagValidation:
			allTags = set()
			print('In Progress Tag Validation. This may take some time depending on the XML file size.....')
			for event, elem in self.context:
				allTags.add(elem.tag)

			for each in self.tags:
				if each not in allTags:
					raise ValueError('Given tags are not present in XML')

	def parse(self):
		pass

	def export_dataset(self):
		pass


def main():
	DataFramerXML('../../gurugram.osm', ['q'])


if __name__ == '__main__':
	main()
