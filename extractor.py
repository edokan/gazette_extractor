#!/usr/bin/python3
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET, lxml.etree, sys, argparse

parser = argparse.ArgumentParser(description="Extractor of features included in .xml file od djvu format")
parser.add_argument('-p', help = "Path to .xml file produced from djvu")
args = parser.parse_args()

tree = ET.parse(args.p)
root = tree.getroot()

for word in root.iter('WORD'):
    if not word: coordinates = list(word.attrib.values())[0].split(',')
    x1 = coordinates[0]
    y1 = coordinates[1]
    x2 = coordinates[2]
    y2 = coordinates[3]
    print("\t".join([str(x1), str(y1), str(x2), str(y2)]))
    
