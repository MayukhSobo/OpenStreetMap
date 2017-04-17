import xml.etree.cElementTree as ET
import os
import inspect
PWD = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def gather_for_observation(root, child, typeof, files, mapToOrig):
	if typeof not in ['all', 'unique']:
		raise NotImplementedError('{} typeof is not known'.format(typeof))
	if typeof == 'all':
		collected_data_keys = list()
		collected_data_values = list()
	elif typeof == 'unique':
		collected_data_keys = set()
		collected_data_values = set()
	if child == '*':
		for each in files:
			context = iter(ET.iterparse(os.path.join(PWD, '..', '..', 'res', each),
												events=('start', 'end')))
			for event, elem in context:
				if event == 'end' and elem.tag == root:
					if typeof == 'all':
						for child in elem:
							if child.tag == 'tag':
								collected_data_keys.append(child.get('k'))
								collected_data_values.append(child.get('v'))
							elif child.tag == 'nd':
								collected_data_keys.append('ref')
								collected_data_values.append(child.get('ref'))
					elif typeof == 'unique':
						for child in elem:
							if child.tag == 'tag':
								collected_data_keys.add(child.get('k'))
								collected_data_values.add(child.get('v'))
							elif child.tag == 'nd':
								collected_data_keys.add('ref')
								collected_data_values.add(child.get('ref'))
	if typeof == 'all':
		# This is memory inefficient. Use 'grouped' for better memory performance
		return [dict([i]) for i in zip(collected_data_keys, collected_data_values)]
	else:
		return collected_data_keys, collected_data_values


def gather_for_cleaning(root, child, typeof, files, mapToOrig):
	for each in files:
		context = iter(ET.iterparse(os.path.join(PWD, '..', '..', 'res', each),
													events=('start', 'end')))
		_, r = next(context)
		for event, elem in context:
			if root == 'node':
				# {changeset: 505778, id: 1331, lat: 34.24, lon: 24.23, k: [], v: []}
				ret_elem = {'changeset': None, 'id': None, 'lat': None, 'lon': None, 'user': None, 'type': None, 'k': [], 'v': []}
			elif root == 'way':
				# {changeset: 505778, id: 1331, user: "Mayukh", refs: [], k: [], v: []}
				ret_elem = {'changeset': None, 'id': None, 'user': None, 'type': None, 'refs': [], 'k': [], 'v': []}
			if event == 'end' and elem.tag == root:
				ret_elem['changeset'] = int(elem.get('changeset'))
				ret_elem['id'] = int(elem.get('id'))
				ret_elem['user'] = elem.get('user')

				if root == 'node':
					ret_elem['lat'] = float(elem.get('lat'))
					ret_elem['lon'] = float(elem.get('lon'))
				for child in elem:
					if child.tag == 'tag':
						ret_elem['k'].append(child.get('k'))
						ret_elem['v'].append(child.get('v'))
					if root == 'way' and child.tag == 'nd':
						ret_elem['refs'].append(int(child.get('ref')))
				ret_elem['type'] = str(root)
				yield ret_elem
				r.clear()
