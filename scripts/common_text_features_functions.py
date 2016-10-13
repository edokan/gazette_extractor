#!/usr/bin/python3                                                                                                                                                                              
# -*- coding: utf-8 -*-       

"""Module which contains functions which are used more than once in text features extraction scripts
"""

import xml.etree.ElementTree as ET
import string

def cut_xml(_x1, _y1, _x2, _y2, root):
    """Returns text, contained in specified area (recognized rectangle in newspaper), from xml file.
       Args:                                                                                                 
           _x1, _y1, _x2, _y2 : coordinates of area (recognized rectangle in newspaper).
    """
    words_list = []
    for word in root.iter('WORD'):
        if word.text is not None:
            coordinates = list(word.attrib.values())[0].split(',')
            x1 = coordinates[0]
            y1 = coordinates[1]
            x2 = coordinates[2]
            y2 = coordinates[3]
            if (int(x1) > int(_x1) and int(x2) < int(_x2) and int(y1) > int(_y1) and int(y2) < int(_y2) and word.text is not None):
                words_list.append(word.text.strip())
    return words_list

def get_punct_amount(words_list):
    """Returns number of punctation in rectangle                                                                                                                                  
       Args:                                                                                                                                                                
           words_list : list of words in which we need to check amount of punctation
    """
    count = lambda l1, l2: len(list(filter(lambda c: c in l2, l1)))
    return sum([count(word, string.punctuation) for word in words_list])
