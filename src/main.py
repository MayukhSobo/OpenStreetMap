import inspect
import os
import sys
from termcolor import colored
from dataClean import Cleaner
from dataFrame import DataFramerXML
from dataExport import Exporter
from dataAudit import validate

PWD = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.append(os.path.join(PWD, 'dataFrame'))
sys.path.append(os.path.join(PWD, 'dataAudit'))
sys.path.append(os.path.join(PWD, 'dataClean'))
sys.path.append(os.path.join(PWD, 'dataExport'))


def main():
	#########################
	# This is data framing
	print(colored("[>>>>>>>> INFO!! <<<<<<<<]", "blue", attrs=['bold']) + " Started Data Framing")
	tags = ('node', 'way', 'relation')
	files = {'data10.osm': 10, 'data100.osm': 100, 'data1000.osm': 1000, 'data10000.osm': 10000}
	p = DataFramerXML.DataFramerXML(sys.argv[1], tags=tags, files=files)
	p.export_dataset()
	#########################
	print(sys.path)
	print(colored("[>>>>>>>> INFO!! <<<<<<<<]", "blue", attrs=['bold']) + " Started Data Auditing")
	validate.Validate(files=[sys.argv[1]], user='uid',
									location=['lat', 'lon'],
									node='tag', way=['tag', 'nd'],
									map_to_original=False)
	########################
	print(colored("[>>>>>>>> INFO!! <<<<<<<<]", "blue", attrs=['bold']) + " Started Data Cleaning")
	clean = Cleaner.Cleaner()
	node_data, way_data = clean.clean()
	print(colored("[>>>>>>>> INFO!! <<<<<<<<]", "blue", attrs=['bold']) + " Started Data Extaction and Storage")
	# ########################
	export = Exporter.Exporter(node_data, way_data, exporter_format='json')
	node_export_file = export.write('node', file='export_node.json', indent=2)
	way_export_file = export.write('way', file='export_way.json', indent=2)
	# ####  This can only be used if 'exporter_format'='json' in Exporter ###
	print(colored("[>>>>>>>> INFO!! <<<<<<<<]", "blue", attrs=['bold']) + " Started storing data into database...This may take some time!!")
	export.save(database='mongoDB', export_files=(node_export_file, way_export_file), database_name='udacity', placeholder='openStreetDataMap')
	#######################


if __name__ == '__main__':
	if len(sys.argv) == 1:
		raise AttributeError("Usage: ./autorun.sh osmfile")
	main()
