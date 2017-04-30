import json
from pprint import pprint


# with open('test.json', 'w') as json_file:
# 	json_file.write('{\n')
# 	json_file.write('	"name": "Mayukh"')
# 	json_file.write('\n}')

with open('../export/export_way.json') as json_file:
	data = iter(json.load(json_file))

pprint(data)
