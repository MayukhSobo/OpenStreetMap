
# OpenStreetMap
> **Note:** Before porting the code one should take a good look into the location and some location specific cleaning and location specific operations.  

Table of Contents
=================
 * [Introduction](#introduction)
 * [Introduction](#project-structure)
 * [Scripts](#scripts)


## Introduction

Data wrangle of Open Street Map data. This is location agnostic or rather it is developed in almost location agnostic way. The data cleaning process is always dependent on the exact data and in this particular case the location that you choose. I have chosen the location which used to be the place I loved and I stayed. I still love that place but don't stay there although I hope to shift there again. The city name is _Gurgaon_ which is renamed into _Gurugram_. It is one of the developed city in the northern part of the country having highest per capita income as of 2017 and one of the fastest growing city.

## Project Structure

The project is designed as modular as possible. Almost all my project structures look like this. The structure is as follows

 - **export -** This directory contains the project report is pdf, markdown and html format

 - **raw_data -** This contains the raw data of the OpenStreetDataMap file. This is single/multiple bz2 compressed file. Any place osm file
   should be put in this directory
   
 - **res -** This contains the scaled downed version of the main data source and also the decompressed file. All the operation is performed
   from the files here. This directory may not be present at first and
   created by `configure` script.

 -  **test -** Contains all the unit test cases. The code validations can be preformed here. Code coverage is not covered.

## Scripts
