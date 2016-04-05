#!/usr/bin/python3
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET, lxml.etree, sys, argparse

parser = argparse.ArgumentParser(description="Extractor of features included in .xml file od djvu format")
parser.add_argument('path_to_file', help = "Path to .xml file produced from djvu")
args = parser.parse_args()
tree = ET.parse(args.path_to_file)
root = tree.getroot()

for word in root.iter('WORD'):
    coordinates = list(word.attrib.values())[0].split(',')
    x1 = coordinates[0]
    y1 = coordinates[1]
    x2 = coordinates[2]
    y2 = coordinates[3]
    height = float(coordinates[1]) - float(coordinates[3])
    width = float(coordinates[2]) - float(coordinates[0])
    print ("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" %(word.text, x1, y1, x2, y1, x1, y2, x2, y2, height, width))
