from termcolor import colored
from . import generic
from . import fixAmenity
from dataAudit import validate


class Cleaner(object):

	def __init__(self):
		self.node_data = validate.Validate.gather(root='node', typeof='grouped')
		self.way_data = validate.Validate.gather(root='way', typeof='grouped')

	def clean(self):
		# Removing all the nodes having no 'names' except some few
		searchMatchTag = ['amenity', 'highway', ('landuse', 'commercial')]
		data_node = self.node_data
		data_way = self.way_data
		for tag in searchMatchTag:
			data_node = generic.clean_nodes_no_names(tag, data_node)
			data_way = generic.clean_nodes_no_names(tag, data_way)
		self.node_data = data_node
		self.way_data = data_way
		print(colored("[DONE✓]", "green", attrs=['bold']) + " Cleaning for no names")
		self.node_data = generic.expand_country_name('addr:country', 'India', self.node_data)
		self.way_data = generic.expand_country_name('addr:country', 'India', self.way_data)
		print(colored("[DONE✓]", "green", attrs=['bold']) + " Cleaning for Country name")
		self.way_data = generic.detect_area_from_way(self.way_data)
		print(colored("[DONE✓]", "green", attrs=['bold']) + " Marking the area")
		# ###### Fixing the religion #######
		# Perfromed both on node & way ####
		self.node_data = fixAmenity.fixReligion(self.node_data)
		self.way_data = fixAmenity.fixReligion(self.way_data)
		print(colored("[DONE✓]", "green", attrs=['bold']) + " Cleaning the religion tags")
		# ###### Fixing the atms and banks #########
		# Only nodes have bank/atm information ####

		# _____ extracting atms from banks ____ #
		self.node_data = fixAmenity.extractAtms(self.node_data)
		print(colored("[DONE✓]", "green", attrs=['bold']) + " Extraction of atms from bank")
		# ______ unifying 'name' & 'operator' ____ #
		self.node_data = fixAmenity.fixAtms(self.node_data)
		print(colored("[DONE✓]", "green", attrs=['bold']) + " Fixing the atm format")
		# _____ unifying atm & bank 'name' _____#
		self.node_data = fixAmenity.NameUnify(self.node_data, 'bank')
		self.node_data = fixAmenity.NameUnify(self.node_data, 'atm')
		print(colored("[DONE✓]", "green", attrs=['bold']) + " Unification of bank and atm names")
		# ______ merging bar and pub togather ____ #
		self.node_data = fixAmenity.mergeBARnPUB(self.node_data)
		print(colored("[DONE✓]", "green", attrs=['bold']) + " Combining the bar and pub")
		self.node_data = fixAmenity.unifyFuel(self.node_data)
		self.way_data = fixAmenity.unifyFuel(self.way_data)
		print(colored("[DONE✓]", "green", attrs=['bold']) + " Unification of fuel stations")
		self.node_data = fixAmenity.createCuisine(self.node_data)
		self.way_data = fixAmenity.createCuisine(self.way_data)
		print(colored("[DONE✓]", "green", attrs=['bold']) + " Implementing cuisine for restaurants")
		self.node_data = generic.fixAddress(self.node_data)
		self.way_data = generic.fixAddress(self.way_data)
		print(colored("[DONE✓]", "green", attrs=['bold']) + " Fixing the address of all nodes and ways")
		self.node_data = generic.removeHindiNames(self.node_data)
		self.way_data = generic.removeHindiNames(self.way_data)
		self.node_data = generic.removeIsINs(self.node_data)
		self.way_data = generic.removeIsINs(self.way_data)
		print(colored("[DONE✓]", "green", attrs=['bold']) + " Fixing problamatic characters in tags and/or values")
		self.node_data = generic.removeBackSlashes(self.node_data)
		self.way_data = generic.removeBackSlashes(self.way_data)
		print(colored("[DONE✓]", "green", attrs=['bold']) + " Removing backslashes form the strings")
		self.node_data = generic.removeQuotes(self.node_data)
		self.way_data = generic.removeQuotes(self.way_data)
		print(colored("[DONE✓]", "green", attrs=['bold']) + " Removing Quotes from strings")
		return self.node_data, self.way_data


# if __name__ == '__main__':
# 	validate.Validate.verification_status_node = True
# 	validate.Validate.verification_status_way = True
# 	validate.Validate.files = ['data1000.osm']
# 	c = Cleaner()
# 	c.clean()
