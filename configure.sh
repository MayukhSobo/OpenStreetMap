if [ -d "raw_data" ]; then
	# unpack the osm compressed file
	bzip2 -d "raw_data/gurugram.osm.bz2"
fi