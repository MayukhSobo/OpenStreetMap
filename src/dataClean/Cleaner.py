import sys
import os
import inspect


PWD = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.append(os.path.join(PWD, '..'))
sys.path.append(os.path.join(PWD))
from dataAudit import validate
from generic import clean_nodes_no_names
from fixAmenity import fixReligion, fixAtms
# print(sys.path)


class Cleaner(object):

	def __init__(self):
		# self.supported_operations = ['add_field', 'remove_entry', 'extract',
		# 														'replace', 'fix', 'merge', 'change_field']
		# for each in operation_map:
		# 	if [*each[1].keys()][0] != 'operation':
		# 		raise SyntaxError('Error in operation_map syntax')
		# 	if each[1]['operation'] not in self.supported_operations:
		# 		e = 'Operation \'{}\' is not implemented'.format(each[1]['operation'])
		# 		raise NotImplementedError(e)
		# self.operation_map = operation_map
		self.node_data = validate.Validate.gather(root='node', typeof='grouped')
		self.way_data = validate.Validate.gather(root='way', typeof='grouped')

	def clean(self):
		# Removing all the nodes having no 'names' except some few
		searchMatchTag = ['amenity', 'highway', ('landuse', 'commercial')]
		data_node = self.node_data
		data_way = self.way_data
		for tag in searchMatchTag:
			data_node = clean_nodes_no_names(tag, data_node)
			data_way = clean_nodes_no_names(tag, data_way)
		self.node_data = data_node
		self.way_data = data_way
		# ###### Fixing the religion #######
		self.node_data = fixReligion(self.node_data)
		self.way_data = fixReligion(self.way_data)
		# ###### Fixing the atms #########
		self.node_data = fixAtms(self.node_data)
		self.way_data = fixAtms(self.way_data)

		return self.node_data, self.way_data


if __name__ == '__main__':
	validate.Validate.verification_status_node = True
	validate.Validate.verification_status_way = True
	validate.Validate.files = ['data1000.osm']
	c = Cleaner(a)
	c.clean()
