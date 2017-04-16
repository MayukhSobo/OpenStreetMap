import xml.etree.cElementTree as ET
import os


def gather_nodes(child, typeof, files, mapToOrig):
	if typeof not in ['unique', 'pair', 'all']:
		raise NotImplementedError('{} typeof is not known'.format(typeof))
	collected_data_keys = list()
	collected_data_values = list()
	if child == '*':
		for each in files:
			context = iter(ET.iterparse(os.path.join('..', '..', 'res', each),
												events=('start', 'end')))
			for event, elem in context:
				if event == 'end' and elem.tag == 'node':
					for child in elem:
						collected_data_keys.append(child.get('k'))
						collected_data_values.append(child.get('v'))
	if typeof == 'pair':
		return {k: v for k, v in zip(collected_data_keys, collected_data_values)}
	elif typeof == 'all':
		return [dict([i]) for i in zip(collected_data_keys, collected_data_values)]
	else:
		return set(collected_data_keys), set(collected_data_values)
