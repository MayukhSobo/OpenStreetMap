from . import userValidate
from . import locValidate
from . import observation
from . import gather


class Validate(object):

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
