import inspect
import os
from termcolor import colored
import xml.etree.cElementTree as ET
PWD = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def validate_location(what, which, files, mapToOrig):
	if mapToOrig:
		if files:
			print(colored("[**WARNING!!**]", "yellow", attrs=['bold']) + " map_to_original is true..Ignoring the files")
		files = ['gurugram.osm']
	for each in files:
		context = iter(ET.iterparse(os.path.join(PWD, '..', '..', 'res', each),
												events=('start', 'end')))
		for event, elem in context:
			if event == 'end' and elem.tag == 'node':
				lat = elem.get('lat')
				lon = elem.get('lon')
				try:
					float(lat)
					float(lon)
				except ValueError:
					raise ValueError('Fomatting Error in lat or lon')

				try:
					if float(lat) == int(lat) or float(lon) == int(lon):
						raise AttributeError('Location value can not be in integer')
				except ValueError:
					pass
		print(colored("[PASSED✓]", "green", attrs=['bold']) + " Location validation audit")
