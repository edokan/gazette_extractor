#!/usr/bin/python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET, lxml.etree, re, sys

tree = ET.parse(sys.argv[1])
root = tree.getroot()

#Wyrzucanie współrzędnych słów jako krotka krotek
for word in root.iter('WORD'):
    coordinates = word.attrib.values()[0].split(',')
    #"dół" słowa
    x1y1 = [coordinates[0], coordinates[1]]
    x2y1 = [coordinates[2], coordinates[1]]
    #"góra" słowa
    x1y2 = [coordinates[0], coordinates[3]]
    x2y2 = [coordinates[2], coordinates[3]]

    height = float(coordinates[1]) - float(coordinates[3])
    width = float(coordinates[2]) - float(coordinates[0])

    print [word.text, x1y1, x2y1, x1y2, x2y2, height, width]
