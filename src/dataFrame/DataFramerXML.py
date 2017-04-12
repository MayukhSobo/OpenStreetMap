import xml.etree.cElementTree as ET
from abc import ABC, abstractmethod
import os
ROOT = '../../'
RES = os.path.join(ROOT, 'res')


class ParserXML(ABC):

	def __init__(self, osmFile, events=('start', 'end')):
		if osmFile.split('.')[-1].lower() != 'osm':
			raise ValueError('Error in OSM file')
		self.source = osmFile
		self._context = iter(ET.iterparse(self.source, events=events))
		self._check_root()

	@property
	def context(self):
		return self._context

	def _check_root(self):
		_, self.root = next(self._context)
		if self.root.tag.lower() != 'osm':
			raise ValueError('OpenStreetDataMap Error')

	def _get_element(self, tags):
		for event, elem in self.context:
			if event == 'end' and elem.tag in self.tags:
				yield elem
				self.root.clear()

	@abstractmethod
	def export_dataset(default_path):
		pass


class DataFramerXML(ParserXML):

	def __init__(self, osmFile, tags, **kwargs):
		super(self.__class__, self).__init__(osmFile=osmFile)
		self.tags = tags
		self.export_files = kwargs.get('files')
		self.export = kwargs.get('export')
		self.tagValidation = kwargs.get('tagValidation', False)
		self.rootPath = kwargs.get('root', '.')
		self._validate()

	def _validate(self):
		if not self.export:
			pass
		elif self.export is None and self.export_files is not None or self.export is not None and self.export_files is None:
			raise ValueError('Export value and export_files doesn\'t match')

		if self.tagValidation:
			allTags = set()
			print('In Progress Tag Validation. This may take some time depending on the XML file size.....')
			for event, elem in self.context:
				allTags.add(elem.tag)

			for each in self.tags:
				if each not in allTags:
					raise ValueError('Given tags are not present in XML')

	def export_dataset(self, default_path=RES):
		if not os.path.exists(self.rootPath):
			raise IOError('The path doesn\'t exist.')
		for export_file, factor in self.export_files.items():
			if export_file.split('.')[-1] != 'osm':
				raise ValueError('Export files must OSM type')
			with open(os.path.join(default_path, export_file), 'wb') as output:
				output.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
				output.write(b'<osm>\n  ')
				for i, element in enumerate(self._get_element(self.tags)):
					if i % factor == 0:
						output.write(ET.tostring(element, encoding='utf-8'))
				output.write(b'</osm>')
				self._context = iter(ET.iterparse(self.source, events=('start', 'end')))


def main():
	tags = ('node', 'way', 'relation')
	files = {'data10.osm': 10}
	raw_data = os.path.join(RES, 'gurugram.osm')
	p = DataFramerXML(raw_data, tags=tags, files=files)
	p.export_dataset()


if __name__ == '__main__':
	main()
