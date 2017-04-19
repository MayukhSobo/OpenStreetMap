import xml.etree.cElementTree as ET
from termcolor import colored
import os
import inspect
PWD = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def observe(what, files, mapToOrig):
	if mapToOrig:
		if files:
			print(colored("[**WARNING!!**]", "yellow", attrs=['bold']) + " map_to_original is true..Ignoring the files")
		files = ['gurugram.osm']
	if what not in ('node', 'way', 'relation'):
		return None
	for each in files:
		nested_tags = set()
		context = iter(ET.iterparse(os.path.join(PWD, '..', '..', 'res', each),
												events=('start', 'end')))
		for event, elem in context:
			if event == 'end' and elem.tag == what:
				for child in elem:
					nested_tags.add(child.tag)
		return nested_tags


def _verify_node_attribs(mapToOrig, files):
	for each in files:
		context = iter(ET.iterparse(os.path.join(PWD, '..', '..', 'res', each),
												events=('start', 'end')))
		nodeCount = 0
		id_ = set()
		for event, elem in context:
			if event == 'end' and elem.tag == 'node':
				ID = elem.get('id')
				LAT = elem.get('lat')
				LON = elem.get('lon')
				VERSION = elem.get('version')
				CHANGESET = elem.get('changeset')
				USER = elem.get('user')
				UID = elem.get('uid')
				VERSION = elem.get('version')
				TIMESTAMP = elem.get('timestamp')

				nodeCount += 1
				id_.add(ID)
				try:
					int(ID)
				except ValueError:
					# According the OSM XML documentation
					raise ValueError('ID field must be a 64-bit integer')

				if float(LAT) < -90.0000000 or float(LAT) > 90.0000000:
					raise ValueError('Latititude must be in range of -90 to 90')

				if float(LON) < -180.0000000 or float(LON) > 180.0000000:
					raise ValueError('Longitude must be in range of -180 to 180')
				attribs = [ID, LAT, LON, VERSION, CHANGESET, USER, UID, VERSION, TIMESTAMP]
				if None in attribs:
					return False
		if nodeCount != len(id_):
			raise ValueError('Node count does not match with number of unique IDs')
		return True


def _verify_way_attribs(mapToOrig, files):
	for each in files:
		context = iter(ET.iterparse(os.path.join(PWD, '..', '..', 'res', each),
												events=('start', 'end')))
		wayCount = 0
		id_ = set()
		for event, elem in context:
			if event == 'end' and elem.tag == 'way':
				ID = elem.get('id')
				CHANGESET = elem.get('changeset')
				USER = elem.get('user')
				UID = elem.get('uid')
				TIMESTAMP = elem.get('timestamp')
				VERSION = elem.get('version')
				wayCount += 1
				id_.add(ID)
				try:
					int(ID)
				except ValueError:
					# According the OSM XML documentation
					raise ValueError('ID field must be a 64-bit integer')
				attribs = [ID, TIMESTAMP, VERSION, CHANGESET, USER, UID]
				if None in attribs:
					print(attribs)
					return False
		if wayCount != len(id_):
			raise ValueError('Way count does not match with number of unique IDs')
		return True


def verify(what, which, tags_data, mapToOrig, files=None):
	if mapToOrig:
		if files:
			print(colored("[**WARNING!!**]", "yellow", attrs=['bold']) + " map_to_original is true..Ignoring the files")
		files = ['gurugram.osm']
	if what not in ('node', 'way', 'relation'):
		return False

	# for nodes
	if what == 'node':
		# This is because all node tags must have one child named 'tag'
		if len(list(tags_data)) != 1 or list(tags_data)[0] != which:
			raise ValueError("NODE VERIFICATION: Childs of node is Unknown!!")
		if not _verify_node_attribs(mapToOrig, files):
			raise AttributeError("Some node attributes are missing")

	# for ways
	elif what == 'way':
		# This is because all way must have two childs named 'tag' and 'nd'
		if len(list(tags_data)) != 2:
			raise ValueError("WAY VERIFICATION: Error in unique number of child nodes!!")
		if sorted(which) != sorted(list(tags_data)):
			raise ValueError("NODE VERIFICATION: Childs of way is Unknown!!")
		if not _verify_way_attribs(mapToOrig, files):
			raise AttributeError("Some way attributes are missing")

	print(colored("[PASSED✓]", "green", attrs=['bold']) + " {} verification audit".format(what))
	return True
