"""
This files relates with all the cleaning related
to amenity. Not all the amenities are solved but most
relevants are handled here. Among the majorly
handled amenities, the handled ones are 'religion',
'atm', 'bank', 'restaurants', 'fastfood'
"""
import re
searchMatchTag = 'amenity'


def fixReligion(data):
	"""
	This checks if all the nodes and
	ways having an amenity of 'place_of_worship'
	has a tag called 'religion'. This is important
	because without the religion, 'place_of_worship'
	is of no use.
	Here we are checking if the node/way has a religion
	tag. If not then we are trying to predict the religion
	from the name itself.
	:param: data - restructured and verified node data and way data
	"""
	searchMatchValue = 'place_of_worship'
	for each in data:
		if searchMatchTag in each['k'] and searchMatchValue in each['v']:
			tagValueData = dict(zip(each['k'], each['v']))
			if tagValueData.get('religion') is None and each.get('removed') is None:
				# Predict the religion name
				name = tagValueData.get('name')
				hindu = r'([mM]andir|[tT]emple)'
				sikh = r'([Gg]urudwara|[gG]uru|[Gg]obind)'
				jain = r'[jJ]ain'
				if re.findall(hindu, name) != []:
					# ##### Fix for Hindu religion
					each['k'].append('religion')
					each['v'].append('hindu')
				elif re.findall(jain, name) != []:
					# ##### Fix for Jain religion
					each['k'].append('religion')
					each['v'].append('Jain')
				elif re.findall(sikh, name) != []:
					# ##### Fix for Sikh religion
					each['k'].append('religion')
					each['v'].append('Sikh')
				else:
					each['removed'] = 'true'
		yield each


def fixAtms(data):
	"""
	This solves the ambiguity of all the nodes
	having 'amenity' as 'atm' and atm operator name
	distrubuted with both tags, 'name' & 'operator'.
	We need to make it uniform because later on we
	may perform a groupby operations on all the atms
	to find which operator has most atms.
	:param: data - restructured and verified node data and way data
	"""
	searchMatchValue = 'atm'
	for each in data:
		if searchMatchTag in each['k'] and searchMatchValue in each['v']:
			tagValueData = dict(zip(each['k'], each['v']))
			if tagValueData.get('name') is None:
				if tagValueData.get('operator') is None:
					each['removed'] = 'true'
				else:
					each['k'][each['k'].index('operator')] = 'name'
		yield each
