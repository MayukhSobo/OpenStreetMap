def fixReligion(options, node_data, way_data):
	searchMatchTag = 'amenity'
	searchMatchValue = 'place_of_worship'
	for each in node_data:
		if searchMatchTag in each['k'] and searchMatchValue in each['v']:
			tagValueData = dict(zip(each['k'], each['v']))
			if tagValueData.get('religion') is None:
				# religion is not present..predict religion from name
				pass
