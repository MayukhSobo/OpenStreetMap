import inspect
import os
import xml.etree.cElementTree as ET
PWD = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def gather_for_observation(root, child, typeof, files):
	'''
	This collects the data points mentioned by 'root'
	from the XML raw data using the dataFrame section
	into respective data formats. The data can be fetched
	by different method. The 'child' parameter indicateds
	that what are the sub nodes of the 'root' should be parsed.
	Currently '*' is used to indicate all the sub nodes of the
	root is used. Other values can be used if we want to neglect
	any particular sub node of a node but currently not implemented.
	The 'typeof' is used to parse the data and store it in different
	format. The following are the specification
		typeof = 'all' means all the tag and value pairs would be
		returned in a list. Here same tag and value pair would be
		put multiple times. For example,
				[{"amenity": "school"}, ..., {"amenity": "school"}]
		this is only good to have a complete/detailed overview of the
		tag and values. But for a large file, this is memory inefficient.
	For better performance, we should use 'unique' to observe the unique
	tag and values.

	Overall, this is important becuase to perform data cleaning operation,
	the data needs to be observed first to check if there is anything wrong.
	This function does exactly that. However this function is not used in
	actual process from 'main.py'.

	:param: root      - data needs to be parsed
	:param: child     - sub nodes that is to be parsed
	:param: typeof 	  - how the data to be parsed ('all', 'unique')
	:param: files  	  - file(s) to be parsed
	'''
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
								# This is for node
								collected_data_keys.append(child.get('k'))
								collected_data_values.append(child.get('v'))
							elif child.tag == 'nd':
								# THis is for way
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
		# This is memory inefficient.
		return [dict([i]) for i in zip(collected_data_keys, collected_data_values)]
	else:
		return collected_data_keys, collected_data_values


def gather_for_cleaning(root, files):
	'''
	This collects data for cleaning purpose
	with and performs a similar operation
	like 'gather_for_observation()' only
	with the following differences
		a. It actively uses the iterator and hence very memory efficient
		b. It uses a constant 'typeof' called 'gropued'
		c. It yields a node or a way in dict data from which is easy to
			mould in JSON data from

	:param: root - Data points to be parsed
	:param: files - Files to be parsed
	'''
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
