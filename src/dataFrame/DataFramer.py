import xml.etree.cElementTree as ET
from abc import ABC, abstractmethod


class Parser(ABC):
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

	def _check_root(self):
		if self.root.tag.lower() != 'osm':
			raise ValueError('OpenStreetDataMap Error')

	@abstractmethod
	def parse(self):
		pass

	@abstractmethod
	def export_dataset(fraction):
		pass


def main():
	Parser('../../gurugram.osm')


if __name__ == '__main__':
	main()
