from . import userValidate
from . import locValidate
from . import observation
from . import gather


class Validate(object):
	'''
	This verifies the data for the
	the docmentation and level of validation
	scoped by the documentation. This checks before
	cleaning the data if it has any logical errors
	which is not following the documentation page.
	Cleaning of logically wrong data is not possible
	because it follows perfectly data formats and
	data patterns. Hence validation functions like
	'validate_user', 'validate_location' & 'verify'
	validates a particular field in data or the
	complete data.

	This also sets the following flags
		'verification_status_node'
		'verification_status_way'
	for better communication with the
	dataClean module.
	'''

	verification_status_node = False
	verification_status_way = False
	files = None
	map_to_original = False

	def __init__(self, files=None, **kwargs):
		self.validators = list()
		Validate.map_to_original = kwargs.get('map_to_original', False)
		for what, which in kwargs.items():
			self.validators.append({what: which})

		if files is None and not Validate.map_to_original:
			raise ValueError("Files can not be None if map_to_original is false")
		else:
			Validate.files = files
		self._validate(Validate.map_to_original)

	def _validate(self, mapToOrig):
		for each in self.validators:
			what = [*each.keys()][0]
			which = [*each.values()][0]

			# >>>>>>>>>>>>>  VALIDATIONS <<<<<<<<<<<<<< #

			# --------- USER validation --------- #
			if what == 'user':
				userValidate.validate_user(what, which, Validate.files, mapToOrig)
			# ------------------------------------ #

			# -------- LOCATION validation --------#
			if what == 'location':
				locValidate.validate_location(what, which, Validate.files, mapToOrig)
			# -------------------------------------#

			# >>>>>>>>>>>>>  OBSERVATIONS <<<<<<<<<<<<<< #
			tags_data = observation.observe(what, Validate.files, mapToOrig)
			if what == 'node':
				Validate.verification_status_node = observation.verify(what, which, tags_data, mapToOrig, Validate.files)
			elif what == 'way':
				Validate.verification_status_way = observation.verify(what, which, tags_data, mapToOrig, Validate.files)

	@staticmethod
	def gather(root, child='*', typeof='unique'):
		'''
		This is a wrapper function that calls the data collection
		methods for various operations. This is the only wrapper
		that communicates with the 'dataClean' module and pulls
		the raw data in the following format
				-----  Node -----
		{changeset: 505778, id: 1331, lat: 34.24, lon: 24.23, k: [], v: []}
				---- Way ----
		{changeset: 505778, id: 1331, user: "Mayukh", refs: [], k: [], v: []}

		:param: root: data to be gathered ( 'node' or 'way')
		:param: child: sub elements to be gathered (currently '*' means all)
		:param: typeof: How data to be fetched ('unique', 'grouped', 'all')
		'''
		if root == 'node' and not Validate.verification_status_node:
			raise AttributeError("Verification for node was not performed/successful")
		if root == 'way' and not Validate.verification_status_way:
			raise AttributeError("Verification for way was not performed/successful")

		if typeof == 'grouped':
			return gather.gather_for_cleaning(root, child, typeof, Validate.files, Validate.map_to_original)
		else:
			return gather.gather_for_observation(root, child, typeof, Validate.files, Validate.map_to_original)


# def main():
# 	Validate(files=['data10000.osm'], user='uid',
# 									location=['lat', 'lon'],
# 									node='tag')

# 	data = Validate.gather(root='node', typeof='grouped')
# 	for each in data:
# 		print(each)


# if __name__ == '__main__':
# 	main()
