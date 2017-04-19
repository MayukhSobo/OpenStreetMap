from dataFrame import DataFramerXML
from dataAudit import validate
import sys
from termcolor import colored


def main():
	# #This is data framing
	# print(colored("[>>>>>>>> INFO!! <<<<<<<<]", "blue", attrs=['bold']) + " Started Data Framing")
	# tags = ('node', 'way', 'relation')
	# files = {'data10.osm': 10, 'data100.osm': 100, 'data1000.osm': 1000, 'data10000.osm': 10000}
	# p = DataFramerXML.DataFramerXML(sys.argv[1], tags=tags, files=files)
	# p.export_dataset()
	#########################
	# #This is data auditing
	print(colored("[>>>>>>>> INFO!! <<<<<<<<]", "blue", attrs=['bold']) + " Started Data Auditing")
	validate.Validate(files=['data10000.osm'], user='uid',
									location=['lat', 'lon'],
									node='tag', way=['tag', 'nd'],
									map_to_original=False)
	# data = validate.Validate.gather(root='node', typeof='grouped')
	# for each in data:
	# 	print(each)

	# data = validate.Validate.gather(root='way', typeof='grouped')
	# for each in data:
	# 	print(each)
	########################


if __name__ == '__main__':
	main()
