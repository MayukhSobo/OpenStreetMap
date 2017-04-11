#!/bin/sh

if [ -d "raw_data" ]; then
	# unpack the osm compressed file
	FILE_PATH=raw_data/*
	for eachRawFile in $FILE_PATH
	do
		bzip2 -dk $eachRawFile
		IN=$eachRawFile
		set -- "$IN"
		IFS="/"; declare -a Array=($*)
		_FILE=${Array[1]}
		set -- "$_FILE"
		IFS="."; declare -a Array=($*)
		mv raw_data/${Array[0]}.${Array[1]} res/
		IFS=""
	done
fi