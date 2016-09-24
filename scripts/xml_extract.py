#!/usr/bin/python3                                                                                                                                   
# -*- coding: utf-8 -*-      

"""Prints coordinates of paragraphs, words and lines due to given .xml file
   .xml file needs to be cleaned by wrong_chars_xml_cleaner.py
   Helps in checking what is word and what is the picture fragment.
"""
#Skrypt, kory wyrzuca koordynaty slow, paragrafow oraz linii wg podanego xmla
#ROGER THAT: plik xml MUSI byc przepuszczony przez skrypt wrong_chars_xml_cleaner.py, ktory usuwa niedozwolone znaki z pliku xml.

import sys
import xml.etree.ElementTree as ET
import string

try:
    tree_xml = ""
    for line in sys.stdin: tree_xml += line
    root = ET.fromstring(tree_xml)
except:
    exit(0)

para_begin_end = []
output_words_lines = []

def get_punct_amount(txt):
    """Returns punctation amount
       Parameters:
       ----------
       txt : string which needs to be checked
    """
    count = lambda l1, l2: len(list(filter(lambda c: c in l2, l1)))
    return sum([count(word, string.punctuation) for word in txt])

def get_alpha(line):
    """Returns alphanumeric chars amount
       Parameters:
       ----------
       line : string which needs to be checked
    """
    alpha = 0
    for letter in line:
        if letter.isalpha(): alpha += 1
    return alpha

def check_paragraph(para_xml):
    """Checks if paragraphs contains trash, returns true if not and false if yes
       Parameters:
       para_xml : xml of paragraph
    """
    root = ET.fromstring(para_xml)
    text = ""
    for word in root.iter("WORD"):
        if word.text != None: text += word.text
    if get_alpha(text) > get_punct_amount(text): return 1
    else : return 0
    
def create_output():
    """Prints out the final output
    """
    sys.stdout.write("PARAGRAPH\t" + str(para_begin_end[0][0]) + " " + str(para_begin_end[0][1]) + " " + str(para_begin_end[-1][2]) + " " + str(para_begin_end[-1][3]) + "\n")
    for records in output_words_lines : sys.stdout.write(records + "\n")

def create_words_lines_output(coordinates_words):
    """Function which helps in making data for lines and words
    """
    coordinates = []
    for key, value in coordinates_words.items():
        coordinates.append(key)
        para_begin_end.append(key)

    output_words_lines.append("LINE\t" + str(coordinates[0][0]) + " " + str(coordinates[0][1]) + " " + str(coordinates[-1][2]) + " " + str(coordinates[-1][3]))

    for key, value in coordinates_words.items():
        keys = []
        for k in key: keys.append(k)
        output_words_lines.append("WORD\t" + ' '.join(keys) + ' ' + value)

def get_words_xml(line_xml):
    """Get words from .xml
       Parameters:
       ----------
       line_xml : xml of line
    """
    root = ET.fromstring(line_xml)
    coordinates_word = {}
    for word in root.iter("WORD"):
        if not word: 
            coordinates = list(word.attrib.values())[0].split(',')
            x1 = coordinates[0]
            y1 = coordinates[1]
            x2 = coordinates[2]
            y2 = coordinates[3]
            if (word.text != None) :
                coordinates_word[x1,y1,x2,y2] = word.text.lstrip().rstrip()
    if coordinates_word : create_words_lines_output(coordinates_word)

def get_lines_xml(para_xml):
    """Get lines from xml
       Parameters:
       ----------
       para_xml : xml of paragraph
    """
    root = ET.fromstring(para_xml)
    for line in root.iter("LINE"):
        line_xml = ET.tostring(line)
        get_words_xml(line_xml)
        
def get_paragraphs_xml():
    """Get paragraphs from xml
    """
    para_xml = ""
    for line in root.iter("PARAGRAPH"):
        para_xml = ET.tostring(line)        
        if check_paragraph(para_xml):
            get_lines_xml(para_xml)
            create_output()
            para_begin_end[:] = []
            output_words_lines[:] = []

if __name__ == "__main__":
    get_paragraphs_xml()


