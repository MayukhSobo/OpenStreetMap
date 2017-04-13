from userValidate import validate_user
from locValidate import validate_location
from observation import observe_nodes


class Validate(object):

	def __init__(self, files=None, **kwargs):
		self.validators = list()
		for what, which in kwargs.items():
			self.validators.append({what: which})

		if files is None:
			raise ValueError("Files can not be None")
		else:
			self.files = files
		self._validate()
		self.node_data = None

	def _validate(self):
		for each in self.validators:
			what = [*each.keys()][0]
			which = [*each.values()][0]

			# >>>>>>>>>>>>>  VALIDATIONS <<<<<<<<<<<<<< #

			# --------- USER validation --------- #
			if what == 'user':
				validate_user(what, which, self.files)
			# ------------------------------------ #

			# -------- LOCATION validation --------#
			if what == 'location':
				validate_location(what, which, self.files)
			# -------------------------------------#

			# >>>>>>>>>>>>>  OBSERVATIONS <<<<<<<<<<<<<< #
			if what == 'node':
				self.node_data = observe_nodes(what, which, self.files)


def main():
	Validate(files=['data100.osm'], node='tag')


if __name__ == '__main__':
	main()
