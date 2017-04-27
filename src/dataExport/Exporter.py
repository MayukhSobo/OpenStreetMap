import os
import inspect
PWD = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


class Exporter(object):
	def __init__(self, node_data, way_data, exporter_format='json', **kwargs):
		if exporter_format not in ['json', 'database']:
			raise AttributeError('Unknown exporter_format {}'.format(exporter_format))
		self.eformat = exporter_format
		if self.eformat == 'json':
			self.database = kwargs.get('db')
			self.port = kwargs.get('port')
		self.node = node_data
		self.way = way_data

	def write(self, dtype, **kwargs):
		if dtype not in ['node', 'way']:
			raise AttributeError('Unsupported data type')
		if self.eformat == 'json':
			eFile = kwargs.get('file')
			indentLevel = int(kwargs.get('indent'))
			indent = ' ' * indentLevel
			if dtype == 'node':
				# {'changeset': 45923649, 'id': 4675043023, 'lat': 28.4673828, 'lon': 77.0836251, 'user': 'parambyte', 'type': 'node', 'k': [], 'v': []}
				exportDir = os.path.join(PWD, '..', '..', 'export')
				exportFile = os.path.join(exportDir, eFile)
				with open(exportFile, 'w') as exf:
					exf.write('{\n')
					exf.write(indent + '"name": "Mayukh",')
					exf.write('\n}')
				# print(eFile)
