import sys
import os
import inspect
from termcolor import colored

PWD = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.append(os.path.join(PWD, '..'))
sys.path.append(os.path.join(PWD))
from dataAudit import validate
from generic import *
from fixAmenity import *
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
		print(colored("[DONE✓]", "green", attrs=['bold']) + " Cleaning for no names")
		self.node_data = expand_country_name('addr:country', 'India', self.node_data)
		self.way_data = expand_country_name('addr:country', 'India', self.way_data)
		print(colored("[DONE✓]", "green", attrs=['bold']) + " Cleaning for Country name")
		self.way_data = detect_area_from_way(self.way_data)
		print(colored("[DONE✓]", "green", attrs=['bold']) + " Marking the area")
		# ###### Fixing the religion #######
		# Perfromed both on node & way ####
		self.node_data = fixReligion(self.node_data)
		self.way_data = fixReligion(self.way_data)
		print(colored("[DONE✓]", "green", attrs=['bold']) + " Cleaning the religion tags")
		# ###### Fixing the atms and banks #########
		# Only nodes have bank/atm information ####

		# _____ extracting atms from banks ____ #
		self.node_data = extractAtms(self.node_data)
		print(colored("[DONE✓]", "green", attrs=['bold']) + " Extraction of atms from bank")
		# ______ unifying 'name' & 'operator' ____ #
		self.node_data = fixAtms(self.node_data)
		print(colored("[DONE✓]", "green", attrs=['bold']) + " Fixing the atm format")
		# _____ unifying atm & bank 'name' _____#
		self.node_data = NameUnify(self.node_data, 'bank')
		self.node_data = NameUnify(self.node_data, 'atm')
		print(colored("[DONE✓]", "green", attrs=['bold']) + " Unification of bank and atm names")
		# ______ merging bar and pub togather ____ #
		self.node_data = mergeBARnPUB(self.node_data)
		print(colored("[DONE✓]", "green", attrs=['bold']) + " Combining the bar and pub")
		self.node_data = unifyFuel(self.node_data)
		self.way_data = unifyFuel(self.way_data)
		print(colored("[DONE✓]", "green", attrs=['bold']) + " Unification of fuel stations")
		self.node_data = createCuisine(self.node_data)
		self.way_data = createCuisine(self.way_data)
		print(colored("[DONE✓]", "green", attrs=['bold']) + " Implementing cuisine for restaurants")
		self.node_data = fixAddress(self.node_data)
		self.way_data = fixAddress(self.way_data)
		print(colored("[DONE✓]", "green", attrs=['bold']) + " Fixing the address of all nodes and ways")
		self.node_data = removeHindiNames(self.node_data)
		self.way_data = removeHindiNames(self.way_data)
		self.node_data = removeIsINs(self.node_data)
		self.way_data = removeIsINs(self.way_data)
		print(colored("[DONE✓]", "green", attrs=['bold']) + " Fixing problamatic characters in tags and/or values")
		self.node_data = removeBackSlashes(self.node_data)
		self.way_data = removeBackSlashes(self.way_data)
		print(colored("[DONE✓]", "green", attrs=['bold']) + " Removing backslashes form the strings")
		return self.node_data, self.way_data


if __name__ == '__main__':
	validate.Validate.verification_status_node = True
	validate.Validate.verification_status_way = True
	validate.Validate.files = ['data1000.osm']
	c = Cleaner()
	c.clean()
