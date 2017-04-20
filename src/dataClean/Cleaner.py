import sys
import os
import inspect
# from fixAmenity import fixReligion

PWD = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.append(os.path.join(PWD, '..'))
sys.path.append(os.path.join(PWD))
from dataAudit import validate
from generic import clean_nodes_no_names
print(sys.path)
a = [
	(
		{'amenity': 'place_of_worship'},
		{'operation': 'add_field'},
		{'fieldName': 'religion'},
		{'condition': 'false'},
		{'on': 'religion'}
	),

	(
		{'name': '*'},
		{'operation': 'remove_entry'},
		{'condition': 'false'},
		{'on': 'name'}
	),

	(
		{'amenity': 'atm'},
		{'operation': 'extract'},
		{'from': 'amenity > bank'}
	),

	(
		{'addr:country': 'IN'},
		{'operation': 'replace'},
		{'IN': 'India'},
		{'on': 'addr:country'}
	),

	(
		{'addr:postcode': '*'},
		{'operation': 'fix'},
		{'country': 'India'},
		{'on': 'addr:postcode'}
	),

	(
		{'amenity': 'marketplace'},
		{'operation': 'remove_entry'},
		{'condition': 'irrelevant'},
		{'on': 'name'}
	),

	(
		{'amenity': 'bar'},
		{'operation': 'merge'},
		{'into': 'amenity > pub'}
	),

	(
		{'amenity': 'restaurants'},
		{'operation': 'fix'},
		{'on': 'name'}
	),

	(
		{'way': 'ref'},
		{'operation': 'change_field'},
		{'fieldName': 'type'},
		{'condition': 'ref[0] == ref[-1]'},
		{'on': 'type'}
	),
]


class Cleaner(object):

	def __init__(self, operation_map):
		self.supported_operations = ['add_field', 'remove_entry', 'extract',
																'replace', 'fix', 'merge', 'change_field']
		for each in operation_map:
			if [*each[1].keys()][0] != 'operation':
				raise SyntaxError('Error in operation_map syntax')
			if each[1]['operation'] not in self.supported_operations:
				e = 'Operation \'{}\' is not implemented'.format(each[1]['operation'])
				raise NotImplementedError(e)
		self.operation_map = operation_map
		self.node_data = validate.Validate.gather(root='node', typeof='grouped')
		self.way_data = validate.Validate.gather(root='way', typeof='grouped')

	def clean(self):
		# Removing all the nodes having no 'names' except some few
		searchMatchTag = ['amenity', 'highway', ('landuse', 'commercial')]
		data = self.node_data
		for tag in searchMatchTag:
			data = clean_nodes_no_names(tag, data)
		# for each in self.operation_map:
		# 	if each[1]['operation'] == 'add_field':
		# 		self.add_field(each)
		# 	# elif each[1]['operation'] == 'remove_entry':
		# 	# 	self.remove_entry(each)
		# 	# elif each[1]['operation'] == 'extract':
		# 	# 	self.extract(each)
		for each in data:
			print(each)
			# pass

	# def add_field(self, options):
	# 	try:
	# 		if options[-1]['on'] == 'religion':
	# 			fixReligion(options, self.node_data, self.way_data)
	# 	except KeyError:
	# 		raise SyntaxError('Error in operation_map syntax')

	# def remove_entry(self, options):
	# 	print(options)

	# def extract(self, options):
	# 	print(options)


if __name__ == '__main__':
	validate.Validate.verification_status_node = True
	validate.Validate.verification_status_way = True
	validate.Validate.files = ['data10.osm']
	c = Cleaner(a)
	c.clean()
