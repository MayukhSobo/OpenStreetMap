from copy import deepcopy


def clean_nodes_no_names(tag, data):
	if not isinstance(tag, tuple):
		for each in data:
			if each['k'] != [] and each['v'] != []:
				if tag in each['k'] and 'name' not in each['k']:
					each['removed'] = 'true'
					tagValueData = dict(zip(each['k'], each['v']))
					if tagValueData.get('amenity') == 'atm':
						each['removed'] = 'false'
			yield each
	else:
		for each in data:
			if each['k'] != [] and each['v'] != []:
				if tag[0] in each['k'] and tag[1] in each['v'] and 'name' not in each['k']:
					each['removed'] = 'true'
			yield each


def expand_country_name(tag, name, data):
	for each in data:
		if tag in each['k'] and each['v'][each['k'].index(tag)] == 'IN':
			each['v'][each['k'].index(tag)] = name
		yield each


def detect_area_from_way(data):
	for each in data:
		if int(each['refs'][0]) == int(each['refs'][-1]):
			each['type'] == 'area'
		yield each


def fixAddress(data):
	for each in data:
		tempK = list()
		for tag in each['k']:
			if tag.split(':')[0] == 'addr':
				tempK.append(tag.split(':')[1])
			else:
				tempK.append(tag)
			each['k'] = deepcopy(tempK)
		yield each
