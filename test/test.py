#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET  # Use cElementTree or lxml if too slow

OSM_FILE = "../res/gurugram.osm"  # Replace this with your osm file
SAMPLE_FILE = "sample.osm"

k = 10000  # Parameter: take every k-th top level element


context = iter(ET.iterparse(OSM_FILE, events=('start', 'end')))
# _, root = next(context)


def root():
    _, _root = next(context)
    return _root


def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag

    Reference:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """

    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            # root().clear()


root()

with open(SAMPLE_FILE, 'wb') as output:
    output.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write(b'<osm>\n  ')

    # Write every kth top level element
    for i, element in enumerate(get_element(OSM_FILE)):
        if i % k == 0:
            output.write(ET.tostring(element, encoding='utf-8'))

    output.write(b'</osm>')
