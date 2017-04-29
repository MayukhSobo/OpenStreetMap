from copy import deepcopy
import re


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
			each['type'] = 'area'
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


def removeHindiNames(data):
	hi = r"\w+:hi$"
	for each in data:
		k = list(filter(lambda e: re.findall(hi, e) != [], each['k']))
		if k:
			for e in k:
				index = each['k'].index(e)
				each['k'].pop(index)
				each['v'].pop(index)
		yield each


def removeIsINs(data):
	is_in = r"is_in:(\w+)"
	for each in data:
		k = list(filter(lambda e: re.findall(is_in, e) != [], each['k']))
		if k:
			# print(k[0])
			for e in k:
				index = each['k'].index(e)
				each['k'][index] = e.split(':')[-1]
		yield each


def removeBackSlashes(data):
	backslash = r'.*(\\).*'
	for each in data:
		for v in each.values():
			if not isinstance(v, list):
				# Not implemented because not true case
				pass
		tagValueData = dict(zip(each['k'], each['v']))
		for tag, val in tagValueData.items():
			if re.findall(backslash, str(tag)) != []:
				_tag = " ".join(map(lambda e: e.strip(), str(tag).split('\\'))).strip()
				each['k'][each['k'].index(tag)] = _tag
			if re.findall(backslash, str(val)) != []:
				_val = " ".join(map(lambda e: e.strip(), str(val).split('\\'))).strip()
				each['v'][each['v'].index(val)] = _val
		yield each
