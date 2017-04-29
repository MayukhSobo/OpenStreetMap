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
					for each in self.node:
						changeset = each.get('changeset')
						_id = each.get('id')
						lat = each.get('lat')
						lon = each.get('lon')
						user = each.get('user')
						_type = each.get('type')
						removed = each.get('removed')
						# This part is constant for all nodes
						if removed is None or removed == 'false':
							exf.write('{\n')
							exf.write(indent + '"id": ' + str(_id) + ',\n')
							exf.write(indent + '"type": ' + '"' + str(_type) + '",\n')
							exf.write(indent + '"position": [' + str(lat) + ', ' + str(lon) + '],\n')
							# This part is not constant for all the nodes
							tagValueData = dict(zip(each['k'], each['v']))
							for tag, value in tagValueData.items():
								exf.write(indent + '"' + str(tag) + '": "' + str(value) + '",\n')
							# This part is also constant for all nodes
							exf.write(indent + '"created": ' + '{\n')
							exf.write(indent * 2 + '"changeset": ' + str(changeset) + ',\n')
							exf.write(indent * 2 + '"user": ' + '"' + str(user) + '"\n')
							exf.write(indent + '}')
							# exf.write(indent + '"lon": ' + str(lon) + ',\n')
							exf.write(indent + '\n},\n')
			elif dtype == 'way':
				pass
