from . import userValidate
from . import locValidate
from . import observation
from . import gather


class Validate(object):

	verification_status = False
	files = None
	map_to_original = False

	def __init__(self, files=None, **kwargs):
		self.validators = list()
		Validate.map_to_original = kwargs.get('map_to_original', False)
		for what, which in kwargs.items():
			self.validators.append({what: which})

		if files is None:
			raise ValueError("Files can not be None")
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
			# For node
			node_data = observation.observe(what, Validate.files, mapToOrig)
			Validate.verification_status = observation.verify(what, which, node_data, mapToOrig, Validate.files)
			# For way

	@staticmethod
	def gather(root, child='*', typeof='unique'):
		if root == 'node':
			if not Validate.verification_status:
				raise AttributeError("Verification for {} was not performed".format(root))
			if typeof == 'grouped':
				return gather.gather_nodes_for_cleaning(child, typeof, Validate.files, Validate.map_to_original)
			else:
				return gather.gather_nodes_for_observation(child, typeof, Validate.files, Validate.map_to_original)


# def main():
# 	Validate(files=['data10000.osm'], user='uid',
# 									location=['lat', 'lon'],
# 									node='tag')

# 	data = Validate.gather(root='node', typeof='grouped')
# 	for each in data:
# 		print(each)


# if __name__ == '__main__':
# 	main()
