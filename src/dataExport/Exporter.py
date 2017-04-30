import os
import inspect
import json
from termcolor import colored
PWD = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


class Exporter(object):
	mongo_json = False

	def __init__(self, node_data, way_data, exporter_format='json', **kwargs):
		if exporter_format not in ['json', 'mongo_json']:
			raise AttributeError('Unknown exporter_format {}'.format(exporter_format))
		self.eformat = exporter_format
		# %%%%%% For future use to any other database %%%%%% #
		# // TODO Support MongoDB or MySQL support directly without export files
		if self.eformat == 'database':
			self.database = kwargs.get('db')
			self.port = kwargs.get('port')
		# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
		if self.eformat == 'mongo_json':
			Exporter.mongo_json = True
		self.node = node_data
		self.way = way_data

	def write(self, dtype, **kwargs):
		if dtype not in ['node', 'way']:
			raise AttributeError('Unsupported data type')
		if self.eformat in ['json', 'mongo_json']:
			exportDir = os.path.join(PWD, '..', '..', 'export')
			eFile = kwargs.get('file')
			exportFile = os.path.join(exportDir, eFile)
			indentLevel = int(kwargs.get('indent'))
			indent = ' ' * indentLevel
			if dtype == 'node':
				# {'changeset': 45923649, 'id': 4675043023, 'lat': 28.4673828, 'lon': 77.0836251, 'user': 'parambyte', 'type': 'node', 'k': [], 'v': []}
				with open(exportFile, 'w') as exf:
					if not Exporter.mongo_json:
						exf.write('[\n')
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
							exf.write(indent + '{\n')
							exf.write(indent * 2 + '"id": ' + str(_id) + ',\n')
							exf.write(indent * 2 + '"type": ' + '"' + str(_type) + '",\n')
							exf.write(indent * 2 + '"position": [' + str(lat) + ', ' + str(lon) + '],\n')
							# This part is not constant for all the nodes
							tagValueData = dict(zip(each['k'], each['v']))
							for tag, value in tagValueData.items():
								exf.write(indent * 2 + '"' + str(tag) + '": "' + str(value) + '",\n')
							# This part is also constant for all nodes
							exf.write(indent * 2 + '"created": ' + '{\n')
							exf.write(indent * 3 + '"changeset": ' + str(changeset) + ',\n')
							exf.write(indent * 3 + '"user": ' + '"' + str(user) + '"\n')
							exf.write(indent * 2 + '}')
							# exf.write(indent + '"lon": ' + str(lon) + ',\n')
							if not Exporter.mongo_json:
								exf.write('\n' + indent + '},' + '\n')
							else:
								exf.write('\n' + indent + '}' + '\n')
					if not Exporter.mongo_json:
						exf.seek(exf.tell() - 2)
						exf.write('\n]\n')
			elif dtype == 'way':
				with open(exportFile, 'w') as exf:
					if not Exporter.mongo_json:
						exf.write('[\n')
					for each in self.way:
						# {'changeset': 21141423, 'id': 122980960, 'user': "n'garh", 'type': 'area', 'refs': [1372597048, 1372597058, 1372597060, 1372597055, 1372597048], 'k': ['name', 'landuse'], 'v': ['Super Mart I', 'retail']}
						changeset = each.get('changeset')
						_id = each.get('id')
						user = each.get('user')
						_type = each.get('type')
						refs = each.get('refs')
						removed = each.get('removed')
						if removed is None or removed == 'false':
							# This part is constant
							exf.write(indent + '{\n')
							exf.write(indent * 2 + '"id": ' + str(_id) + ',\n')
							exf.write(indent * 2 + '"type": ' + '"' + str(_type) + '",\n')
							exf.write(indent * 2 + '"refs": [ ')
							# And this part is not
							# #### Writing the references ####
							for ref in refs:
								exf.write(str(ref) + ', ')
							exf.seek(exf.tell() - 2)
							exf.write(' ],\n')
							# ##### Writing other tags-values ######
							tagValueData = dict(zip(each['k'], each['v']))
							for tag, value in tagValueData.items():
								exf.write(indent * 2 + '"' + str(tag) + '": "' + str(value) + '",\n')
							# This part is also constant
							exf.write(indent * 2 + '"created": ' + '{\n')
							exf.write(indent * 3 + '"changeset": ' + str(changeset) + ',\n')
							exf.write(indent * 3 + '"user": ' + '"' + str(user) + '"\n')
							exf.write(indent * 2 + '}')
							if not Exporter.mongo_json:
								exf.write('\n' + indent + '},' + '\n')
							else:
								exf.write('\n' + indent + '}' + '\n')
					if not Exporter.mongo_json:
						exf.seek(exf.tell() - 2)
						exf.write('\n]\n')
			print(colored("[DONE✓]", "green", attrs=['bold']) + " Created the export file {}".format(eFile))
			return exportFile

	def save(self, database, export_files, **kwargs):
		# ######### Here other database can be supported ###########
		if database.lower() not in ['mongodb']:
			raise NotImplementedError('Can not find the driver for the database {}'.format(database))
		with open(export_files[0]) as json_file:
				try:
					node_data = iter(json.load(json_file))
				except ValueError:
					raise SyntaxError('Export JSON file is not formatted properly.')
		print(colored("[DONE✓]", "green", attrs=['bold']) + " Passed the validation of node export file")
		with open(export_files[1]) as json_file:
				try:
					way_data = iter(json.load(json_file))
				except ValueError:
					raise SyntaxError('Export JSON file is not formatted properly.')
		print(colored("[DONE✓]", "green", attrs=['bold']) + " Passed the validation of way export file")
		if database.lower() == 'mongodb':
			from pymongo import MongoClient
			databaseName = kwargs.get('database_name')
			collection = kwargs.get('placeholder')
			client = MongoClient('localhost', 27017)
			db = client[databaseName]
			# Drop the collection if exists already
			db.drop_collection(collection)
			for node in node_data:
				db[collection].insert_one(node)
			for way in way_data:
				db[collection].insert_one(way)
