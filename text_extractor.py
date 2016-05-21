#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import xml.etree.ElementTree as ET
import string
import argparse

words_counter = 0
lines_counter = 0
chars_counter = 0
punct_counter = 0 
letters_counter = 0
count = lambda l1, l2: len(list(filter(lambda c: c in l2, l1)))

parser = argparse.ArgumentParser(description="Extractor of text features included in .xml file od djvu format")
parser.add_argument('p', help = "Path to .xml file produced from djvu")
parser.add_argument('o', help = "File name where output will be kept")
parser.add_argument('--c', help = "Coordinates mode - write to file coordinates of words")
parser.add_argument('--tf', help = "Text features mode - write to file number of : words, lines, chars, punctations, letters")
args = parser.parse_args()

tree = ET.parse(args.p)
root = tree.getroot()

for word in root.iter('WORD'):
    if args.tf: 
        chars_counter += len(word.text)
        punct_counter += count(word.text, string.punctuation)

    if args.c:
        if not word: coordinates = list(word.attrib.values())[0].split(',')
        x1 = coordinates[0]
        y1 = coordinates[1]
        x2 = coordinates[2]
        y2 = coordinates[3]
        print("\t".join([str(x1), str(y1), str(x2), str(y2)]))


if args.tf:
    for line in open(args.p):
        line = line.rstrip()
        if ("<WORD" in line): words_counter += 1
        if ("<LINE>" in line): lines_counter += 1

    if (chars_counter - punct_counter < 0): letters_counter = 0
    else : letters_counter = chars_counter - punct_counter

    with open(args.o, 'w') as output:
        output.write("WORDS_COUNTER=%s\nLINES_COUNTER=%s\nCHARS_COUNTER=%s\nPUNCT_COUNTER=%s\nLETTERS_COUNTER=%s\n" % (words_counter, lines_counter, chars_counter, punct_counter, letters_counter))

