import xml.etree.cElementTree as ET
import os


def observe_nodes(what, which, files):
	for each in files:
		nested_tags = set()
		context = iter(ET.iterparse(os.path.join('..', '..', 'res', each),
												events=('start', 'end')))
		for event, elem in context:
			if event == 'end' and elem.tag == 'node':
				for child in elem:
					nested_tags.add(child.tag)
		print(nested_tags)
