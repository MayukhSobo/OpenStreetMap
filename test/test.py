import xml.etree.cElementTree as ET

osm_file = '../gurugram.osm'

context = iter(ET.iterparse(osm_file, events=('start', 'end')))
_, root = next(context)
tags = ('node', 'way', 'relation')
allTags = set()
for event, elem in context:
	allTags.add(elem.tag)

for each in tags:
	if each not in allTags:
		print('OOPs!!')
# 	if elem.tag == 'way':
# 		print(elem.tag)
# print(root.tag)
