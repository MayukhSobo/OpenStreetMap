
# OpenStreetMap
> **Note:** Before porting the code one should take a good look into the location and some location specific cleaning and location specific operations.  

Table of Contents
=================

<!-- toc orderedList:0 depthFrom:1 depthTo:6 -->

* [OpenStreetMap](#openstreetmap)
* [Table of Contents](#table-of-contents)
    * [1. Introduction](#1-introduction)
    * [2. Project Structure](#2-project-structure)
    * [3. Scripts](#3-scripts)
    * [4. Modules](#4-modules)
    * [5. Data](#5-data)
    * [6. Execution](#6-execution)
    * [7. Export Links](#7-export-links)

<!-- tocstop -->

### 1. Introduction

Data wrangle of Open Street Map data. This is location agnostic or rather it is developed in almost location agnostic way. The data cleaning process is always dependent on the exact data and in this particular case the location that you choose. I have chosen the location which used to be the place I loved and I stayed. I still love that place but don't stay there although I hope to shift there again. The city name is _Gurgaon_ which is renamed into _Gurugram_. It is one of the developed city in the northern part of the country having highest per capita income as of 2017 and one of the fastest growing city.

### 2. Project Structure

The project is designed as modular as possible. Almost all my project structures look like this. The structure is as follows

 - **export -** This directory contains the project report is pdf, markdown and html format

 - **raw_data -** This contains the raw data of the OpenStreetDataMap file. This is single/multiple bz2 compressed file. Any place osm file
   should be put in this directory

 - **res -** This contains the scaled downed version of the main data source and also the decompressed file. All the operation is performed
   from the files here. This directory may not be present at first and
   created by `configure` script.

 -  **test -** Contains all the unit test cases. The code validations can be preformed here. Code coverage is not covered.

## 3. Scripts

There are multiple scripts that can ease the project to a lot extent. The scripts are following

 - **autorun.sh -**
 - **configure.sh -**
 - **export.sh -**
## 4. Modules
The application is comprised of 4 major modules namely, *dataFrame, dataAudit, dataClean, dataExport*. The detailed structure is mentioned below


  - **dataFrame -**   This modules is responsible for low level data handling from the OSM-XML file itself. This can pull data and then scale down the data in different sections like _**data10.osm, data100.osm, data1000.osm etc...**._ Pulling data from API is not yet supported but if later implemented, it should go into this module. Other different data formats should also be supported by this section


  - **dataAudit -** This module is responsible for all the data auditing required before the data cleaning. Unsuccessful data auditing indicates the format of the data to be incorrect and hence data cleaning is not performed even if the cleaning module is used.


  - **dataClean -** This module performs the real cleaning operations on the data. The data cleaning is a relative operation which relates to the data to be cleaned and the in this particular cases the area which is mentioned.


  - **dataExport -** Responsible for exporting the data into a json file or into a database. Currently we are using MongoDB but data bases like MySQL can also be used because of the design pattern of the code.

## 5. Data


## 6. Execution


## 7. Export Links
