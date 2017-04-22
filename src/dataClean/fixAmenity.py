"""
This files relates with all the cleaning related
to amenity. Not all the amenities are solved but most
relevants are handled here. Among the majorly
handled amenities, the handled ones are 'religion',
'atm', 'bank', 'restaurants', 'fastfood'
"""
import re
from copy import deepcopy
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
	:param: data - restructured and verified node data
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


def extractAtms(data):
	"""
	It is extracting all the atms from the
	banks. It is taking a node having both
	'atm' and 'bank' and creating two separate
	nodes with two separate 'amenities'
	:param: data - restructured and verified node data
	"""
	searchMatchValue = 'bank'
	for each in data:
		if searchMatchTag in each['k'] and searchMatchValue in each['v']:
			tagValueData = dict(zip(each['k'], each['v']))
			if tagValueData.get('atm') is not None:
				tempEach = deepcopy(each)
				tempEach['v'].pop(tempEach['k'].index('atm'))
				tempEach['k'].remove('atm')
				tempEach['v'][tempEach['k'].index('amenity')] = 'atm'
				# This is for newly created atm node
				yield tempEach
		# This is for the already exixting bank node
		yield each


def NameUnify(data, amenity):
	"""
	This make all the bank or atm names unified.
	This cleaning was important because same banks
	were included with different names which could
	have created problems during later stage. This
	works only on 'bank' and 'atm'. Recommended to
	use only after 'fixAtms()' and 'extractAtms()'

	:param: amenity - can be either 'bank' or 'atm'
	:param: data - restructured and verified node data
	"""
	if amenity not in ['bank', 'atm']:
		raise NotImplementedError("NameUnify can not unity nodes/ways with {}".format(amenity))
	searchMatchValue = amenity
	for each in data:
		if searchMatchTag in each['k'] and searchMatchValue in each['v'] and each.get('removed') != 'true':
			tagValueData = dict(zip(each['k'], each['v']))
			amenityName = tagValueData.get('name')
			# ### Some most common bank/atm operator names ####
			hdfc = len(re.findall(r'([hH][dD][fF][cC])', amenityName)) >= 1
			icici = len(re.findall(r'([iI][cC][iI][cC][iI])', amenityName)) >= 1
			axis = len(re.findall(r'([aA][xX][iI][sS])', amenityName)) >= 1
			citi = len(re.findall(r'([cC][iI][tT][iI])', amenityName)) >= 1
			sbi = len(re.findall(r'([sS][bB][iI]|[sS][tT][aA][tT][eE])', amenityName)) >= 1
			kotak = len(re.findall(r'([kK][oO][tT][aA][kK])', amenityName)) >= 1
			hsbc = len(re.findall(r'[hH][sS][bB][cC]', amenityName)) >= 1
			pnb = len(re.findall(r'([pP][nN][bB]|[pP][uU][nN][jJ][aA][bB])', amenityName)) >= 1
			obc = len(re.findall(r'([Oo][bB][cC]|[Oo][rR][iI][eE][nN][tT][aA][Ll])', amenityName)) >= 1
			boi = len(re.findall(r'([bB][oO][iI]|[iI][nN][dD][iI][aA])', amenityName)) >= 1
			indusland = len(re.findall(r'([iI][nN][dD][uU][sS])', amenityName)) >= 1
			scb = len(re.findall(r'([Cc][hH][aA][rR][tT][eE][rR])', amenityName)) >= 1
			banks = [(hdfc, 'HDFC Bank'), (icici, 'ICICI Bank'), (axis, 'AXIS Bank'), (citi, 'CITI Bank'), (sbi, 'State Bank of India'), (kotak, 'KOTAK MAHINDRA'), (hsbc, 'HSBC Bank'), (pnb, 'Punjab National Bank'), (obc, 'ORIENTAL BANK OF COMMERCE'), (boi, 'BANK OF INDIA'), (indusland, 'INDUSLAND BANK'), (scb, 'Standard Chartated Bank')]
			for bank in banks:
				if bank[0]:
					# Because dicts are passed by reference
					temp = deepcopy(each)
					temp['v'][temp['k'].index('name')] = bank[1]
					# #### For most common bank and atms ####
					yield temp
			if not any([hdfc, icici, axis, citi, sbi, kotak, hsbc, pnb, obc, boi, indusland, scb]):
				# #### For some uncommon banks or atms
				yield each
		else:
			# #### For other nodes ####
			yield each
