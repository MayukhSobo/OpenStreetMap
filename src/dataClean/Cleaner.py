from .. import dataAudit


class Cleaner(object):

	def __init__(self):
		self.supported_operations = ['add', 'remove', 'extract']
