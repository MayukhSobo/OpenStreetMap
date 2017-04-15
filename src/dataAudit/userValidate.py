import xml.etree.cElementTree as ET
import os
from collections import defaultdict
from termcolor import colored


def validate_user(what, which, files, mapToOrig):
	for each in files:
		context = iter(ET.iterparse(os.path.join('..', '..', 'res', each),
												events=('start', 'end')))
		users_as_name = defaultdict(set)
		users_as_id = defaultdict(set)
		for event, elem in context:
			if event == 'end' and elem.tag == 'node':
				users_as_name[elem.get('user')].add(elem.get('uid'))
				users_as_id[elem.get('uid')].add(elem.get('user'))

		for k, v in users_as_name.items():
			if len(v) != 1:
				raise ValueError('User {} has more than one unique IDs'.format(k))

		for k, v in users_as_id.items():
			if len(v) != 1:
				raise ValueError('ID {} has more than one unique Users'.format(k))
		print(colored("[PASSED✓]", "green", attrs=['bold']) + " User validation audit")
