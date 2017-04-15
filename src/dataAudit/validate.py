from userValidate import validate_user
from locValidate import validate_location
from observation import observe, verify


class Validate(object):

	def __init__(self, files=None, **kwargs):
		self.validators = list()
		self.map_to_original = kwargs.get('map_to_original', False)
		for what, which in kwargs.items():
			self.validators.append({what: which})

		if files is None:
			raise ValueError("Files can not be None")
		else:
			self.files = files
		self._validate(self.map_to_original)

	def _validate(self, mapToOrig):
		for each in self.validators:
			what = [*each.keys()][0]
			which = [*each.values()][0]

			# >>>>>>>>>>>>>  VALIDATIONS <<<<<<<<<<<<<< #

			# --------- USER validation --------- #
			if what == 'user':
				validate_user(what, which, self.files, mapToOrig)
			# ------------------------------------ #

			# -------- LOCATION validation --------#
			if what == 'location':
				validate_location(what, which, self.files, mapToOrig)
			# -------------------------------------#

			# >>>>>>>>>>>>>  OBSERVATIONS <<<<<<<<<<<<<< #
			# For node
			node_data = observe(what, which, self.files, mapToOrig)
			verify(what, node_data, mapToOrig, self.files)
			# For way


def main():
	Validate(files=['data1000.osm'], user='uid',
									location=['lat', 'lon'],
									node='tag')


if __name__ == '__main__':
	main()
