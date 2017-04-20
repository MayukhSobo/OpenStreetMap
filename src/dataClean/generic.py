def clean_nodes_no_names(tag, node_data):
	if not isinstance(tag, tuple):
		for each in node_data:
			if each['k'] != [] and each['v'] != []:
				if tag in each['k'] and 'name' not in each['k']:
					each['removed'] = 'true'
					tagValueData = dict(zip(each['k'], each['v']))
					if tagValueData.get('amenity') == 'atm':
						each['removed'] = 'false'
			yield each
	else:
		for each in node_data:
			if each['k'] != [] and each['v'] != []:
				if tag[0] in each['k'] and tag[1] in each['v'] and 'name' not in each['k']:
					each['removed'] = 'true'
			yield each
