#!/usr/bin/python3                                                                                                                                   
# -*- coding: utf-8 -*-      

import sys
import xml.etree.ElementTree as ET
import argparse
import string

tree_xml = ""
for line in sys.stdin: tree_xml += line
root = ET.fromstring(tree_xml)

para_begin_end = []
output_words_lines = []

def get_punct_amount(txt):
    """Sprawdza ilość znaków interpunkcyjnych, następnie ją zwraca"""
    count = lambda l1, l2: len(list(filter(lambda c: c in l2, l1)))
    return sum([count(word, string.punctuation) for word in txt])

def get_alpha(line):
    """Sprawdza ilość znaków alfanumerycznych, następnie je zwraca"""
    alpha = 0
    for letter in line:
        if letter.isalpha(): alpha += 1
    return alpha

def check_paragraph():
    """Sprawdza czy paragraf zawiera śmieci, następnie zawraca prawdę jeśli paragrad nie jest śmieciowy"""
    tree = ET.parse("para_xml_file")
    root = tree.getroot()
    text = ""
    for word in root.iter("WORD"):
        if word.text != None: text += word.text
    if get_alpha(text) > get_punct_amount(text): return 1
    else : return 0
    
def create_output():
    """Tworzy finalny output"""
    print("PARAGRAPH\t" + str(para_begin_end[0][0]) + " " + str(para_begin_end[0][1]) + " " + str(para_begin_end[-1][2]) + " " + str(para_begin_end[-1][3]))
    for records in output_words_lines : print(records)

def create_words_lines_output(coordinates_words):
    """pomocnicza funkcja tworzaca dane dla linii oraz slow"""
    coordinates = []
    for key, value in coordinates_words.items():
        coordinates.append(key)
        para_begin_end.append(key)

    output_words_lines.append("LINE\t" + str(coordinates[0][0]) + " " + str(coordinates[0][1]) + " " + str(coordinates[-1][2]) + " " + str(coordinates[-1][3]))

    for key, value in coordinates_words.items():
        keys = []
        for k in key: keys.append(k)
        output_words_lines.append("WORD\t" + ' '.join(keys) + "\t" + value)

def get_words_xml():
    """funkcja wyłuskująca z xmla słowa"""
    tree = ET.parse("line_xml_file")
    root = tree.getroot()
    coordinates_word = {}
    for word in root.iter("WORD"):
        if not word: 
            coordinates = list(word.attrib.values())[0].split(',')
            x1 = coordinates[0]
            y1 = coordinates[1]
            x2 = coordinates[2]
            y2 = coordinates[3]
            if (word.text != None) : coordinates_word[x1,y1,x2,y2] = word.text
    if coordinates_word : create_words_lines_output(coordinates_word)

def get_lines_xml():
    """funkcja wyłuskująca z xmla linie"""
    tree = ET.parse("para_xml_file")
    root = tree.getroot()
    for line in root.iter("LINE"):
        line_xml = ET.tostring(line)
        with open("line_xml_file", "wb") as output:
            output.write(line_xml)
        get_words_xml()
        
def get_paragraphs_xml():
    para_xml = ""
    for line in root.iter("PARAGRAPH"):
        para_xml = ET.tostring(line)        
        with open("para_xml_file", "wb") as output:
            output.write(para_xml)
        if check_paragraph():
            get_lines_xml()
            create_output()
            para_begin_end[:] = []
            output_words_lines[:] = []

def main():
    get_paragraphs_xml()

main()
