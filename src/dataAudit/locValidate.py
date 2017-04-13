import xml.etree.cElementTree as ET
from termcolor import colored
import os


def validate_location(what, which, files):
	for each in files:
		context = iter(ET.iterparse(os.path.join('..', '..', 'res', each),
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

				if float(lat) == int(lat) and float(lon) == int(lon):
					raise ValueError('Location value can not be in integer')
		print(colored("[PASSED✓]", "green", attrs=['bold']) + " Location validation audit")
