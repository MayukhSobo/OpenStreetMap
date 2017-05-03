
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

 - **configure.sh -** This is used only once before running the project. This install and creates the virtual environment named _'venv'_
 
 - **autorun.sh -**  This runs the project and initiates the complete process. This script should be run with a parameter for the file name. Usually it is the name of the file which is to be used for all the data operations.
## 4. Modules
The application is comprised of 4 major modules namely, *dataFrame, dataAudit, dataClean, dataExport*. The detailed structure is mentioned below


  - **dataFrame -**   This modules is responsible for low level data handling from the OSM-XML file itself. This can pull data and then scale down the data in different sections like _**data10.osm, data100.osm, data1000.osm etc...**._ Pulling data from API is not yet supported but if later implemented, it should go into this module. Other different data formats should also be supported by this section


  - **dataAudit -** This module is responsible for all the data auditing required before the data cleaning. Unsuccessful data auditing indicates the format of the data to be incorrect and hence data cleaning is not performed even if the cleaning module is used.


  - **dataClean -** This module performs the real cleaning operations on the data. The data cleaning is a relative operation which relates to the data to be cleaned and the in this particular cases the area which is mentioned.


  - **dataExport -** Responsible for exporting the data into a json file or into a database. Currently we are using MongoDB but data bases like MySQL can also be used because of the design pattern of the code.

## 5. Data
The data that is currently parsed from the OSM raw_data file and currently _node_ and _way_ is used. The data is parsed into the intermediate form of python dicts. Here is how it looks

### Node
```python
{changeset: 505778, id: 1331, lat: 34.24, lon: 24.23, k: [], v: []}
```
### Way
```python
{changeset: 505778, id: 1331, user: "Mayukh", refs: [], k: [], v: []}
```

After the the cleaning and export stage when it is stored into the JSON file this would look like following
 
### Node
```
{
   "id": 248852574,
   "type": "node",
   "position": [28.533492, 77.1518947],
   "name": "Cafe Coffee Day",
   "amenity": "cafe",
   "created": {
      "changeset": 13836050,
      "user": "Oberaffe"
   }
}
```
### Way
```
{
    "id": 7891819,
    "type": "area",
    "refs": [ 58043990, 58043991, 58043992, 
              58043993, 58043994, 58043995, 
              58043996, 58043997, 58043990 ],
    "name": "School of Computational and Integrative Sciences",
    "amenity": "school",
    "building": "yes",
    "created": {
      "changeset": 18193716,
      "user": "satyaakam"
    }
  }
```
## 6. Execution
To run this project locally ,

_**Step 1:**_ Clone the the project locally

_**Step 2:**_ Ensure ```python3``` is installed in your system. Recommended version is **>= Python 3.6**

_**Step 3:**_ run the bash script as
```sh
$ sh configure.sh

or,

$ ./configure.sh
```
_**Step 4:**_ Activate the virtual environment using the following command
```sh
$ source ./venv/bin/activate
```
_**Step 5:**_ Make sure the database is properly running. In our case, we are currently using _MongoDB_. However the this project can be extended for other databases like _MySQL or Cassandra DB_.

_**Step 6:**_ Execute the autorun script using the following command. It takes a file name as a parameter. This indicates the file name which is used for the data manipulation
```sh
$ sh autorun.sh gurugram.osm

or

$ ./autorun.sh gurugram.osm
``` 

## 7. Export Links

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

 - **configure.sh -** This is used only once before running the project. This install and creates the virtual environment named _'venv'_
 
 - **autorun.sh -**  This runs the project and initiates the complete process. This script should be run with a parameter for the file name. Usually it is the name of the file which is to be used for all the data operations.
## 4. Modules
The application is comprised of 4 major modules namely, *dataFrame, dataAudit, dataClean, dataExport*. The detailed structure is mentioned below


  - **dataFrame -**   This modules is responsible for low level data handling from the OSM-XML file itself. This can pull data and then scale down the data in different sections like _**data10.osm, data100.osm, data1000.osm etc...**._ Pulling data from API is not yet supported but if later implemented, it should go into this module. Other different data formats should also be supported by this section


  - **dataAudit -** This module is responsible for all the data auditing required before the data cleaning. Unsuccessful data auditing indicates the format of the data to be incorrect and hence data cleaning is not performed even if the cleaning module is used.


  - **dataClean -** This module performs the real cleaning operations on the data. The data cleaning is a relative operation which relates to the data to be cleaned and the in this particular cases the area which is mentioned.


  - **dataExport -** Responsible for exporting the data into a json file or into a database. Currently we are using MongoDB but data bases like MySQL can also be used because of the design pattern of the code.

## 5. Data
The data that is currently parsed from the OSM raw_data file and currently _node_ and _way_ is used. The data is parsed into the intermediate form of python dicts. Here is how it looks

### Node
```python
{changeset: 505778, id: 1331, lat: 34.24, lon: 24.23, k: [], v: []}
```
### Way
```python
{changeset: 505778, id: 1331, user: "Mayukh", refs: [], k: [], v: []}
```

After the the cleaning and export stage when it is stored into the JSON file this would look like following
 
### Node
```
{
   "id": 248852574,
   "type": "node",
   "position": [28.533492, 77.1518947],
   "name": "Cafe Coffee Day",
   "amenity": "cafe",
   "created": {
      "changeset": 13836050,
      "user": "Oberaffe"
   }
}
```
### Way
```
{
    "id": 7891819,
    "type": "area",
    "refs": [ 58043990, 58043991, 58043992, 
              58043993, 58043994, 58043995, 
              58043996, 58043997, 58043990 ],
    "name": "School of Computational and Integrative Sciences",
    "amenity": "school",
    "building": "yes",
    "created": {
      "changeset": 18193716,
      "user": "satyaakam"
    }
  }
```
## 6. Execution
To run this project locally ,

_**Step 1:**_ Clone the the project locally

_**Step 2:**_ Ensure ```python3``` is installed in your system. Recommended version is **>= Python 3.6**

_**Step 3:**_ run the bash script as
```sh
$ sh configure.sh

or,

$ ./configure.sh
```
_**Step 4:**_ Activate the virtual environment using the following command
```sh
$ source ./venv/bin/activate
```
_**Step 5:**_ Now its time to decide if you need to only execute the data operations or generate the graph and plots using the _Matplotlib_. If the intention is to only execute the software and not generate the report then do
```sh
$ pip install -r requirement_lite.txt
```
else do,
```sh
$ pip install -r requirement_full.txt
```

_**Step 6:**_ Make sure the database is properly running. In our case, we are currently using _MongoDB_. However the this project can be extended for other databases like _MySQL or Cassandra DB_.

_**Step 7:**_ Execute the autorun script using the following command. It takes a file name as a parameter. This indicates the file name which is used for the data manipulation
```sh
$ sh autorun.sh gurugram.osm

or

$ ./autorun.sh gurugram.osm
``` 
_**Optional Step:**_ If you are insterested to manipulate the ```ipython``` notebook file, then run 
```sh
$ jupyter notebook Report.ipynb
```

## 7. Export Links

**_Raw Data Link in OSM:_**  [Gurugram data](https://s3.amazonaws.com/mapzen.odes/ex_ouzwqdDtxgDAGC3AL9EQoXc6A1TSw.osm.bz2)
**_Report Graphs:_** [Jupyter Notebook Link](http://nbviewer.jupyter.org/github/MayukhSobo/OpenStreetMap/blob/master/Report.ipynb)
**_Curated Report:_** [PDF Report](#)
