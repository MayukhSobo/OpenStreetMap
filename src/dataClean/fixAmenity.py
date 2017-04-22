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


def extractAtms(data):
	"""
	It is extracting all the atms from the
	banks. It is taking a node/way having both
	'atm' and 'bank' and creating two separate
	nodes/ways with two separate 'amenities'
	:param: data - restructured and verified node data and way data
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
	searchMatchValue = amenity
	for each in data:
		if searchMatchTag in each['k'] and searchMatchValue in each['v'] and each.get('removed') != 'true':
			tagValueData = dict(zip(each['k'], each['v']))
			bankName = tagValueData.get('name')
			hdfc = len(re.findall(r'([hH][dD][fF][cC])', bankName)) >= 1
			icici = len(re.findall(r'([iI][cC][iI][cC][iI])', bankName)) >= 1
			axis = len(re.findall(r'([aA][xX][iI][sS])', bankName)) >= 1
			citi = len(re.findall(r'([cC][iI][tT][iI])', bankName)) >= 1
			sbi = len(re.findall(r'([sS][bB][iI]|[sS][tT][aA][tT][eE])', bankName)) >= 1
			kotak = len(re.findall(r'([kK][oO][tT][aA][kK])', bankName)) >= 1
			hsbc = len(re.findall(r'[hH][sS][bB][cC]', bankName)) >= 1
			pnb = len(re.findall(r'([pP][nN][bB]|[pP][uU][nN][jJ][aA][bB])', bankName)) >= 1
			obc = len(re.findall(r'([Oo][bB][cC]|[Oo][rR][iI][eE][nN][tT][aA][Ll])', bankName)) >= 1
			boi = len(re.findall(r'([bB][oO][iI]|[iI][nN][dD][iI][aA])', bankName)) >= 1
			indusland = len(re.findall(r'([iI][nN][dD][uU][sS])', bankName)) >= 1
			scb = len(re.findall(r'([Cc][hH][aA][rR][tT][eE][rR])', bankName)) >= 1
			banks = [(hdfc, 'HDFC Bank'), (icici, 'ICICI Bank'), (axis, 'AXIS Bank'), (citi, 'CITI Bank'), (sbi, 'State Bank of India'), (kotak, 'KOTAK MAHINDRA'), (hsbc, 'HSBC Bank'), (pnb, 'Punjab National Bank'), (obc, 'ORIENTAL BANK OF COMMERCE'), (boi, 'BANK OF INDIA'), (indusland, 'INDUSLAND BANK'), (scb, 'Standard Chartated Bank')]
			for bank in banks:
				if bank[0]:
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
