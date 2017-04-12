from userValidate import validate_user


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

	def _validate(self):
		# print(self.validators)
		for each in self.validators:
			what = [*each.keys()][0]
			which = [*each.values()][0]
			if what == 'user':
				# print(what, self.files)
				validate_user(what, which, self.files)


def main():
	Validate(files=['data10000.osm'], user='uid', location=['lat', 'lon'])


if __name__ == '__main__':
	main()
