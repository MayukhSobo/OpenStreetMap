import xml.etree.cElementTree as ET
import os
import inspect
PWD = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def gather_nodes_for_observation(child, typeof, files, mapToOrig):
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
				if event == 'end' and elem.tag == 'node':
					if typeof == 'all':
						for child in elem:
							collected_data_keys.append(child.get('k'))
							collected_data_values.append(child.get('v'))
					elif typeof == 'unique':
						for child in elem:
							collected_data_keys.add(child.get('k'))
							collected_data_values.add(child.get('v'))
	if typeof == 'all':
		# This is memory inefficient. Use 'grouped' for better memory performance
		return [dict([i]) for i in zip(collected_data_keys, collected_data_values)]
	else:
		return collected_data_keys, collected_data_values


def gather_nodes_for_cleaning(child, typeof, files, mapToOrig):
	for each in files:
		# {changeset: 505778, id: 1331, lat: 34.24, lon: 24.23, k: [], v: []}
		context = iter(ET.iterparse(os.path.join(PWD, '..', '..', 'res', each),
													events=('start', 'end')))
		_, root = next(context)
		for event, elem in context:
			ret_elem = {'changeset': None, 'id': None, 'lat': None, 'lon': None, 'k': [], 'v': []}
			if event == 'end' and elem.tag == 'node':
				ret_elem['changeset'] = int(elem.get('changeset'))
				ret_elem['id'] = int(elem.get('id'))
				ret_elem['lat'] = float(elem.get('lat'))
				ret_elem['lon'] = float(elem.get('lon'))
				for child in elem:
					ret_elem['k'].append(child.get('k'))
					ret_elem['v'].append(child.get('v'))
				yield ret_elem
				root.clear()
