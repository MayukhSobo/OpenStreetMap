from dataFrame import DataFramerXML
from dataAudit import validate
import sys


def main():
	# tags = ('node', 'way', 'relation')
	# files = {'data10.osm': 10, 'data100.osm': 100, 'data1000.osm': 1000, 'data10000.osm': 10000}
	# p = DataFramerXML.DataFramerXML(sys.argv[1], tags=tags, files=files)
	# p.export_dataset()

	validate.Validate(files=['data100.osm'], user='uid',
									location=['lat', 'lon'],
									node='tag')

	data = validate.Validate.gather(root='node', typeof='grouped')
	for each in data:
		print(each)


if __name__ == '__main__':
	main()
