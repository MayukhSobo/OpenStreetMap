from copy import deepcopy
import re


def clean_nodes_no_names(tag, data):
	"""
	This removes all the amenities
	which has no names in it with
	the exception of 'atm'. Because
	'atm' sometime has other tag called
	'operator' in place of 'name' which
	is handled later on
	"""
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
	"""
	This replace the 'tag' with value 'IN'
	into 'name'. This used to replace the
	country name in 'data'
	"""
	for each in data:
		if tag in each['k'] and each['v'][each['k'].index(tag)] == 'IN':
			each['v'][each['k'].index(tag)] = name
		yield each


def detect_area_from_way(data):
	"""
	This marks the 'type' in the
	'data' from 'way' to 'area' if
	the first and the last reference
	value is same.
	"""
	for each in data:
		if int(each['refs'][0]) == int(each['refs'][-1]):
			each['type'] = 'area'
		yield each


def fixAddress(data):
	"""
	This fixing the address in 'data'
	converting "addr:tag" into "tag"
	"""
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
	"""
	Removing the hindi name that are present
	in the form of "name:hi". Hindi names are
	removed because hindi names are not required
	and it is not useful too. Moreover, it may
	create problems in json/mongo database
	"""
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
	"""
	Some tags and values in 'data' are
	in the form of "is_in:tag" or "is_in:val".
	These are replaced into "tag" or "val" only
	"""
	is_in = r"is_in:(\w+)"
	for each in data:
		k = list(filter(lambda e: re.findall(is_in, e) != [], each['k']))
		if k:
			for e in k:
				index = each['k'].index(e)
				each['k'][index] = e.split(':')[-1]
		yield each


def removeBackSlashes(data):
	"""
	This removes backslashes from
	everywhere because backslashes
	creates problem in json file or
	in mongoDB
	"""
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


def removeQuotes(data):
	"""
	This removes double quotes from
	everywhere because double quotes
	creates problem in json file or
	in mongoDB
	"""
	for each in data:
		for v in each.values():
			if not isinstance(v, list):
				# Not implemented because not true case
				pass
		tagValueData = dict(zip(each['k'], each['v']))
		for tag, val in tagValueData.items():
			if str(tag).find('"') != -1:
				_tag = str(tag).replace('"', '')
				each['k'][each['k'].index(tag)] = _tag
			if str(val).find('"') != -1:
				_val = str(val).replace('"', '')
				each['v'][each['v'].index(val)] = _val
		yield each
